"""Load the repository configuration."""

import json
from pathlib import Path

CONFIG_PATH = Path(__file__).resolve().parent.parent / 'config.json'


def load_config(path=CONFIG_PATH):
    """Return the raw config object from *path*."""
    with path.open(encoding='utf-8') as config_file:
        return json.load(config_file)


def load_period_config(path=CONFIG_PATH):
    """Return the enabled periods and their display settings."""
    config = load_config(path)
    periods = []
    labels = {}
    colors = {}

    for key, options in config['periods'].items():
        if options.get('enabled', True):
            periods.append(key)
            labels[key] = {'emoji': options['emoji'], 'name': options['name']}
            colors[key] = int(options['color'].lstrip('#'), 16)

    return (
        periods,
        labels,
        colors,
        config.get('max_per_period', 3),
        config.get('blacklist', []),
        config.get('show_flagged_content', False),
    )
