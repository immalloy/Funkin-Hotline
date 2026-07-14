import json
import urllib.request
try:
    from config import load_period_config
except ImportError:  # Also support imports through the src package.
    from src.config import load_period_config

GAME_ID = 8694
TOP_SUBS_URL = f'https://gamebanana.com/apiv12/Game/{GAME_ID}/TopSubs'

PERIODS, LABELS, COLORS, MAX_PER_PERIOD, BLACKLIST, SHOW_FLAGGED = load_period_config()

def _is_blacklisted(mod):
    name = (mod.get('_sName') or '').lower()
    author = (mod.get('_aSubmitter', {}).get('_sName') or '').lower()
    for term in BLACKLIST:
        if term.lower() in name or term.lower() in author:
            return True
    return False

def fetch_top_subs():
    req = urllib.request.Request(TOP_SUBS_URL, headers={'User-Agent': 'Funkin-Hotline/1.0'})
    with urllib.request.urlopen(req, timeout=15) as resp:
        data = json.loads(resp.read())

    result = {p: [] for p in PERIODS}
    for item in data:
        period = item.get('_sPeriod')
        if period not in PERIODS:
            continue
        # Apply filters before the limit so a flagged/blacklisted entry does
        # not consume a slot that could be filled by the next API result.
        if not SHOW_FLAGGED and item.get('_sInitialVisibility') != 'show':
            continue
        if _is_blacklisted(item):
            continue
        if len(result[period]) < MAX_PER_PERIOD:
            result[period].append(item)
    return result

def get_mod_key(mod):
    if not mod:
        return None
    return f'{mod["_sPeriod"]}:{mod["_idRow"]}'

def get_state_key(mods):
    key = {}
    for p in PERIODS:
        ids = [get_mod_key(m) for m in mods[p] if m]
        key[p] = ','.join(ids) if ids else None
    return key

def get_label(period):
    return LABELS.get(period, {'emoji': '', 'name': period})

def get_color(period):
    return COLORS.get(period, 0x5865f2)
