import io
import urllib.request

UA = 'Funkin-Hotline/1.0'

try:
    from PIL import Image
    HAS_PIL = True
except ImportError:
    HAS_PIL = False

AVATAR_SIZE = 56
SHADOW_OFFSET = 3
SHADOW_OPACITY = 0.3

def _load_avatar(url):
    req = urllib.request.Request(url, headers={'User-Agent': UA})
    with urllib.request.urlopen(req, timeout=10) as resp:
        av = Image.open(io.BytesIO(resp.read())).convert('RGBA')
    return av.resize((AVATAR_SIZE, AVATAR_SIZE))

def _paste_avatar(img, av):
    x, y = 6, img.height - AVATAR_SIZE - 6
    shadow = Image.new('RGBA', av.size, (0, 0, 0, 0))
    shadow.putalpha(av.getchannel('A').point(lambda a: int(a * SHADOW_OPACITY)))
    img.paste(shadow, (x + SHADOW_OFFSET, y + SHADOW_OFFSET), shadow)
    img.paste(av, (x, y), av)

def _center_crop_square(img, size):
    w, h = img.size
    min_dim = min(w, h)
    left = (w - min_dim) // 2
    top = (h - min_dim) // 2
    return img.crop((left, top, left + min_dim, top + min_dim)).resize((size, size))

def create_collage(mods, size=240, verbose=False):
    if not HAS_PIL:
        return None

    images = []
    for mod in mods:
        url = mod.get('_sImageUrl')
        if not url:
            continue
        try:
            req = urllib.request.Request(url, headers={'User-Agent': UA})
            with urllib.request.urlopen(req, timeout=10) as resp:
                img = Image.open(io.BytesIO(resp.read())).convert('RGBA')
            img = _center_crop_square(img, size)

            submitter = mod.get('_aSubmitter', {})
            av_url = submitter.get('_sAvatarUrl')
            if av_url and 'defaults/avatar' not in av_url:
                try:
                    _paste_avatar(img, _load_avatar(av_url))
                except Exception as exc:
                    if verbose:
                        print(f'[warn] avatar skipped for {mod.get("_sName", "unknown mod")!r}: {exc}')
            images.append(img)
        except Exception as exc:
            if verbose:
                print(f'[warn] collage image skipped for {mod.get("_sName", "unknown mod")!r}: {exc}')

    if not images:
        return None

    total_w = sum(img.width for img in images)
    max_h = max(img.height for img in images)
    collage = Image.new('RGBA', (total_w, max_h), (0, 0, 0, 0))
    x = 0
    for img in images:
        collage.paste(img, (x, 0), img)
        x += img.width

    buf = io.BytesIO()
    collage.save(buf, format='PNG')
    buf.seek(0)
    return buf
