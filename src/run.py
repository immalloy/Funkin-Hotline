import sys
from gamebanana import fetch_top_subs, get_state_key, PERIODS
from discord import post_to_discord
from state import get_state, save_state

def main():
    mods = fetch_top_subs()
    new_state = get_state_key(mods)
    prev_state = get_state() or {}

    changed_mods = {}
    discord_ids = {}
    for period in PERIODS:
        discord_key = f'discord_{period}'
        if prev_state.get(discord_key):
            discord_ids[discord_key] = prev_state[discord_key]
        if new_state.get(period) != prev_state.get(period) or not prev_state.get(discord_key):
            changed_mods[period] = mods.get(period, [])
        else:
            changed_mods[period] = []

    if any(changed_mods.get(period) for period in PERIODS):
        discord_ids.update(post_to_discord(changed_mods, prev_state))
        print('[ok] discord')
    else:
        print('[ok] discord skipped')

    new_state.update(discord_ids)
    save_state(new_state)
    print('[done] state saved')

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f'[fatal] {e}', file=sys.stderr)
        sys.exit(1)
