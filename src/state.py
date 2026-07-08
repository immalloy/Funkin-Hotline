import json
import os

STATE_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'state.json')

def get_state():
    try:
        with open(STATE_PATH) as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return None

def save_state(state):
    with open(STATE_PATH, 'w') as f:
        json.dump(state, f, separators=(',', ':'))
