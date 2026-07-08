# Funkin Hotline

![banner](assets/banner.png)

Posts the top FNF mods from GameBanana to a Discord channel every 2 hours. Shows the best mods of all time, year, 6 months, 3 months, month, week, and today with a little image collage.

this is just a fun thing. commit names are stupid and vary. i don't take this project seriously.

## live view

[Join the server](https://discord.gg/yQvZ69fsm3)  [#fnf-hotline](https://discord.com/channels/1447703759638626327/1524145705936097351)

## structure

```
├── src/           python source
├── assets/        images
├── scripts/       utility scripts
├── state.json     tracks last posted mods
└── .github/
    └── workflows/ github actions cron
```

## how to fork & use

1. **Fork** this repo on GitHub
2. **Create a Discord webhook** in your server channel → copy the URL
3. Go to your fork → **Settings → Secrets and variables → Actions** → add `DISCORD_WEBHOOK_URL` with your webhook URL
4. Go to **Actions** tab → enable workflows → run "Funkin Mod Rankings" manually to test
5. It'll auto-run every 30 minutes after that

### reset state

Clears `state.json` so the next run posts fresh Discord messages:

```bash
# windows
powershell ./scripts/reset-state.ps1

# linux/macos
bash ./scripts/reset-state.sh
```

that's it.
