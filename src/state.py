import json
from pathlib import Path

STATE_PATH = Path(__file__).resolve().parent.parent / 'state.json'

def get_state(path=None):
    try:
        with Path(path or STATE_PATH).open(encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return None

def save_state(state, path=None):
    state_path = Path(path or STATE_PATH)
    state_path.parent.mkdir(parents=True, exist_ok=True)
    with state_path.open('w', encoding='utf-8') as f:
        json.dump(state, f, separators=(',', ':'))
