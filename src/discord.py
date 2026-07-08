import json
import os
import uuid
import urllib.request
from urllib.error import HTTPError
from gamebanana import PERIODS, get_label, get_color
from collage import create_collage

UA = 'Funkin-Hotline/1.0'
MEDALS = ['\U0001f947', '\U0001f948', '\U0001f949']

def _esc(s):
    return str(s).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')

def _parse_webhook_url(url):
    parts = url.strip('/').split('/')
    return parts[-2], parts[-1]

def _build_embed(period, mods, attachment_name=None):
    label = get_label(period)
    lines = []
    for i, mod in enumerate(mods):
        medal = MEDALS[i] if i < len(MEDALS) else f'{i+1}.'
        author = mod['_aSubmitter']['_sName']
        mod_url = mod['_sProfileUrl']
        safe_name = _esc(mod['_sName']).replace('[', '\\[').replace(']', '\\]')
        lines.append(f'{medal} **[{safe_name}]({mod_url})** by {_esc(author)}')

    embed = {
        'title': f'{label["emoji"]} {label["name"]}',
        'description': '\n'.join(lines),
        'color': get_color(period),
        'footer': {'text': 'Funkin Hotline'},
        'timestamp': __import__('datetime').datetime.now().isoformat() + 'Z',
    }
    if attachment_name:
        embed['image'] = {'url': f'attachment://{attachment_name}'}
    return embed

def _req(url, data=None, method='POST'):
    headers = {'Content-Type': 'application/json', 'User-Agent': UA}
    body = json.dumps(data).encode() if data else None
    return urllib.request.Request(url, data=body, headers=headers, method=method)

def _req_multipart(url, fields, image_bytes, filename, method='POST'):
    boundary = uuid.uuid4().hex
    body = b''

    body += f'--{boundary}\r\n'.encode()
    body += f'Content-Disposition: form-data; name="file"; filename="{filename}"\r\n'.encode()
    body += b'Content-Type: image/png\r\n\r\n'
    body += image_bytes
    body += b'\r\n'

    body += f'--{boundary}\r\n'.encode()
    body += b'Content-Disposition: form-data; name="payload_json"\r\n\r\n'
    body += json.dumps(fields).encode()
    body += b'\r\n'

    body += f'--{boundary}--\r\n'.encode()

    headers = {
        'Content-Type': f'multipart/form-data; boundary={boundary}',
        'User-Agent': UA,
    }
    return urllib.request.Request(url, data=body, headers=headers, method=method)

def _send(period, period_mods, filename, existing_id, base):
    image_buf = create_collage(period_mods)
    image_bytes = image_buf.read() if image_buf else None

    embed = _build_embed(period, period_mods, filename if image_bytes else None)
    msg_id = existing_id

    if existing_id:
        try:
            if image_bytes:
                req = _req_multipart(f'{base}/messages/{existing_id}', {'embeds': [embed]}, image_bytes, filename, 'PATCH')
            else:
                req = _req(f'{base}/messages/{existing_id}', {'embeds': [embed]}, 'PATCH')
            with urllib.request.urlopen(req, timeout=15):
                pass
        except HTTPError as e:
            if e.code == 404:
                msg_id = None
            else:
                raise RuntimeError(f'Discord edit error {e.code}: {e.read().decode()}')

    if not msg_id:
        if image_bytes:
            req = _req_multipart(f'{base}?wait=true', {'embeds': [embed], 'username': 'Funkin Hotline'}, image_bytes, filename)
        else:
            req = _req(f'{base}?wait=true', {'embeds': [embed], 'username': 'Funkin Hotline'})
        with urllib.request.urlopen(req, timeout=15) as resp:
            result = json.loads(resp.read())
            msg_id = result['id']

    return msg_id

def post_to_discord(mods, prev_state):
    wh_url = os.environ.get('DISCORD_WEBHOOK_URL')
    if not wh_url:
        return {}

    wh_id, wh_token = _parse_webhook_url(wh_url)
    base = f'https://discord.com/api/webhooks/{wh_id}/{wh_token}'
    message_ids = {}

    for period in PERIODS:
        period_mods = mods.get(period, [])
        if not period_mods:
            continue

        filename = f'collage_{period}.png'
        existing_id = prev_state.get(f'discord_{period}') if prev_state else None

        try:
            msg_id = _send(period, period_mods, filename, existing_id, base)
        except Exception as e:
            print(f'[warn] failed to post {period}: {e}')
            msg_id = existing_id

        message_ids[f'discord_{period}'] = msg_id

    return message_ids
