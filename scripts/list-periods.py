import sys
sys.path.insert(0, __file__ + '/../..')

from src.gamebanana import PERIODS, LABELS, COLORS, MAX_PER_PERIOD, TOP_SUBS_URL
import json, urllib.request

# Show current config
print('CURRENT CONFIG')
print('=' * 50)
print(f'max_per_period: {MAX_PER_PERIOD}')
print()
for p in PERIODS:
    l = LABELS[p]
    c = COLORS[p]
    print(f'  {l["emoji"]}  {p:8s}  {l["name"]:20s}  #{c:06x}')
print()

# Fetch API to show all available periods
print()
print('PERIODS AVAILABLE FROM API')
print('=' * 50)
req = urllib.request.Request(TOP_SUBS_URL, headers={'User-Agent': 'Funkin-Hotline/1.0'})
with urllib.request.urlopen(req, timeout=15) as resp:
    data = json.loads(resp.read())

seen = {}
for item in data:
    p = item.get('_sPeriod')
    if p not in seen:
        seen[p] = 1
    else:
        seen[p] += 1

for p in sorted(seen.keys()):
    enabled = 'ENABLED' if p in PERIODS else 'DISABLED (set enabled: true in config.json to enable)'
    print(f'  {p:8s}  ({seen[p]} mods)  {enabled}')

print()
print('Edit config.json to enable/disable, rename, or recolor periods.')
