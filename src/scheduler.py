"""Scheduling helpers for the self-hosted runner."""

import sys
import time


def run_forever(run_once, interval_hours):
    """Run *run_once* immediately and repeat it at the configured interval."""
    if interval_hours <= 0:
        raise ValueError('--interval-hours must be greater than zero')

    interval_seconds = interval_hours * 60 * 60
    print(f'[ok] loop started; running every {interval_hours:g} hour(s)')
    while True:
        try:
            run_once()
        except Exception as exc:
            print(f'[fatal] run failed: {exc}', file=sys.stderr)
        print(f'[ok] next run in {interval_hours:g} hour(s)')
        time.sleep(interval_seconds)
