import sys
from gamebanana import fetch_top_subs, get_state_key, PERIODS
from discord import post_to_discord
from state import get_state, save_state

def main():
    mods = fetch_top_subs()
    new_state = get_state_key(mods)
    prev_state = get_state()

    discord_ids = post_to_discord(mods, prev_state or {})
    new_state.update(discord_ids)
    print('[ok] discord')
    save_state(new_state)
    print('[done] state saved')

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f'[fatal] {e}', file=sys.stderr)
        sys.exit(1)
