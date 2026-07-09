import json
import os

STATE_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'state.json')

def get_state(path=None):
    try:
        with open(path or STATE_PATH, encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return None

def save_state(state, path=None):
    state_path = path or STATE_PATH
    parent = os.path.dirname(os.path.abspath(state_path))
    os.makedirs(parent, exist_ok=True)
    with open(state_path, 'w', encoding='utf-8') as f:
        json.dump(state, f, separators=(',', ':'))
