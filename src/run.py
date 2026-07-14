import argparse
import os
import sys
from gamebanana import fetch_top_subs, get_state_key, PERIODS
from discord import post_to_discord
from collage import create_collage
from scheduler import run_forever
from state import get_state, save_state

def parse_args():
    parser = argparse.ArgumentParser(description='Post GameBanana FNF rankings to Discord.')
    parser.add_argument('--dry-run', action='store_true', help='Create local collage previews without posting or changing state.')
    parser.add_argument('--output-dir', default='local-previews', help='Directory for dry-run collage PNGs (default: local-previews).')
    parser.add_argument('--state-file', help='Use a different state file, useful for local testing.')
    parser.add_argument('--verbose', action='store_true', help='Show individual image-download failures.')
    parser.add_argument('--loop', action='store_true', help='Keep running and update rankings on an interval.')
    parser.add_argument('--interval-hours', type=float, default=1, help='Hours between loop runs (default: 1).')
    return parser.parse_args()

def write_previews(mods, output_dir, verbose=False):
    os.makedirs(output_dir, exist_ok=True)
    created = 0
    for period in PERIODS:
        period_mods = mods.get(period, [])
        if not period_mods:
            continue
        image = create_collage(period_mods, verbose=verbose)
        if not image:
            print(f'[warn] no collage created for {period}')
            continue
        output_path = os.path.join(output_dir, f'collage_{period}.png')
        with open(output_path, 'wb') as output:
            output.write(image.read())
        print(f'[ok] preview {output_path}')
        created += 1
    print(f'[done] created {created} local preview(s)')

def run_once(args):
    mods = fetch_top_subs()
    print(f'[ok] fetched {sum(len(items) for items in mods.values())} mod(s) across {len(PERIODS)} period(s)')
    if args.dry_run:
        write_previews(mods, args.output_dir, args.verbose)
        return

    new_state = get_state_key(mods)
    prev_state = get_state(args.state_file) or {}

    changed_mods = {}
    change_counts = {}
    discord_ids = {}
    for period in PERIODS:
        discord_key = f'discord_{period}'
        if prev_state.get(discord_key):
            discord_ids[discord_key] = prev_state[discord_key]
        if new_state.get(period) != prev_state.get(period) or not prev_state.get(discord_key):
            changed_mods[period] = mods.get(period, [])
            old_ids = (prev_state.get(period) or '').split(',')
            new_ids = (new_state.get(period) or '').split(',')
            change_counts[period] = sum(
                old != new for old, new in zip(old_ids, new_ids)
            ) + abs(len(old_ids) - len(new_ids))
        # Unchanged periods are omitted so Discord does not edit them. An
        # empty list is meaningful only when the period itself changed.

    # A period can change from populated to empty when GameBanana changes its
    # result counts. That still needs a Discord edit to clear the old embed.
    periods_need_update = any(
        new_state.get(period) != prev_state.get(period)
        or not prev_state.get(f'discord_{period}')
        for period in PERIODS
    )
    if periods_need_update:
        discord_ids.update(post_to_discord(changed_mods, prev_state, args.verbose, change_counts))
        print('[ok] discord')
    else:
        print('[ok] discord skipped')

    new_state.update(discord_ids)
    save_state(new_state, args.state_file)
    print('[done] state saved')

def main():
    args = parse_args()
    if not args.loop:
        run_once(args)
        return

    run_forever(lambda: run_once(args), args.interval_hours)

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f'[fatal] {e}', file=sys.stderr)
        sys.exit(1)
