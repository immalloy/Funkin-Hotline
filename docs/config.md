# config

Edit `config.json` in the repo root.

## periods

```json
"periods": {
  "alltime": { "enabled": true,  "name": "Best of All Time",   "emoji": "\ud83d\udc51", "color": "#e74c3c" },
  "year":    { "enabled": true,  "name": "Best of the Year",   "emoji": "\ud83c\udfc5", "color": "#e91e63" },
  "6month":  { "enabled": true,  "name": "Best of 6 Months",   "emoji": "\ud83d\udcc5", "color": "#00bcd4" },
  "3month":  { "enabled": true,  "name": "Best of 3 Months",   "emoji": "\ud83d\udcc6", "color": "#4caf50" },
  "month":   { "enabled": true,  "name": "Best of the Month",  "emoji": "\ud83c\udfc6", "color": "#9b59b6" },
  "week":    { "enabled": true,  "name": "Best of the Week",   "emoji": "\ud83d\udd25", "color": "#e67e22" },
  "today":   { "enabled": true,  "name": "Best of Today",      "emoji": "\u2b50",      "color": "#f1c40f" }
}
```

Each entry:
- `enabled` — `false` to hide this period entirely
- `name` — displayed in the embed title
- `emoji` — shown before the name
- `color` — hex color for the embed accent bar

See what periods the API actually returns:

```bash
python scripts/list-periods.py
```

## max per period

```json
"max_per_period": 3
```

How many mods to show per period (1–3).

## term blacklist

```json
"blacklist": ["nsfw", "18+", "gore", "some-author-name"]
```

Mods whose name or author contains any term are skipped. The next available mod from the API takes their place.
