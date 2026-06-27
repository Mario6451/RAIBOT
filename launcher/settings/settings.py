import json
import os

def load_settings():
    path = os.path.join(os.path.dirname(__file__), "settings.json")
    if not os.path.exists(path):
        return {}
    with open(path, "r") as f:
        return json.load(f)

def save_settings(data):
    path = os.path.join(os.path.dirname(__file__), "settings.json")
    with open(path, "w") as f:
        json.dump(data, f, indent=4)
