import json
import urllib.request

GAME_ID = 8694
TOP_SUBS_URL = f'https://gamebanana.com/apiv12/Game/{GAME_ID}/TopSubs'
PERIODS = ['alltime', 'year', '6month', '3month', 'month', 'week', 'today']
MAX_PER_PERIOD = 3

LABELS = {
    'alltime': {'emoji': '\U0001f451', 'name': 'Best of All Time'},
    'year':    {'emoji': '\U0001f3c5', 'name': 'Best of the Year'},
    '6month':  {'emoji': '\U0001f4c5', 'name': 'Best of 6 Months'},
    '3month':  {'emoji': '\U0001f4c6', 'name': 'Best of 3 Months'},
    'month':   {'emoji': '\U0001f3c6', 'name': 'Best of the Month'},
    'week':    {'emoji': '\U0001f525', 'name': 'Best of the Week'},
    'today':   {'emoji': '\u2b50',    'name': 'Best of Today'},
}

COLORS = {
    'alltime': 0xe74c3c,
    'year':    0xe91e63,
    '6month':  0x00bcd4,
    '3month':  0x4caf50,
    'month':   0x9b59b6,
    'week':    0xe67e22,
    'today':   0xf1c40f,
}

def fetch_top_subs():
    req = urllib.request.Request(TOP_SUBS_URL, headers={'User-Agent': 'Funkin-Hotline/1.0'})
    with urllib.request.urlopen(req, timeout=15) as resp:
        data = json.loads(resp.read())

    result = {p: [] for p in PERIODS}
    for item in data:
        period = item.get('_sPeriod')
        if period in PERIODS and len(result[period]) < MAX_PER_PERIOD:
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
