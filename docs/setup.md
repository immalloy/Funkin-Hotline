# setup

1. **Fork** this repo on GitHub
2. **Create a Discord webhook** in your server channel → copy the URL
3. Go to your fork → **Settings → Secrets and variables → Actions** → add `DISCORD_WEBHOOK_URL` with your webhook URL
4. Go to **Actions** tab → enable workflows → run "Funkin Mod Rankings" manually to test
5. It'll auto-run every 2 hours after that

## reset state

Clears `state.json` so the next run posts fresh Discord messages:

```bash
# windows
powershell ./scripts/reset-state.ps1

# linux/macos
bash ./scripts/reset-state.sh
```
