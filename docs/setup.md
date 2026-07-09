# setup

1. **Fork** this repo on GitHub
2. **Create a Discord webhook** in your server channel → copy the URL
3. Go to your fork → **Settings → Secrets and variables → Actions** → add `DISCORD_WEBHOOK_URL` with your webhook URL
4. Go to **Actions** tab → enable workflows → run "Funkin Mod Rankings" manually to test
5. It'll auto-run every 2 hours after that

## self-hosting

To run the bot continuously from your own PC or server instead of GitHub Actions, install Python 3.12+ and Pillow, then set your webhook URL as an environment variable:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
$env:DISCORD_WEBHOOK_URL = 'https://discord.com/api/webhooks/...'
python src/run.py --loop
```

The process runs immediately, then every two hours. Keep it running with a service manager appropriate for the host (for example, Task Scheduler on Windows or systemd on Linux). Use `--interval-hours 1` to change the interval.

Do not run this at the same time as GitHub Actions with the same webhook; choose one host so they do not compete to update the messages.

## reset state

Clears `state.json` so the next run posts fresh Discord messages:

```bash
# windows
powershell ./scripts/reset-state.ps1

# linux/macos
bash ./scripts/reset-state.sh
```
