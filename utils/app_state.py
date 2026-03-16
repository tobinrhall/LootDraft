import json
import os


SAVE_FILE = "saves/run_data.json"


def load_app_state():
    if not os.path.exists(SAVE_FILE):
        return {
            "best_round": 0,
            "best_class": "None"
        }

    try:
        with open(SAVE_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except (json.JSONDecodeError, OSError):
        return {
            "best_round": 0,
            "best_class": "None"
        }


def save_app_state(data):
    os.makedirs("saves", exist_ok=True)

    with open(SAVE_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)