# training/imitation.py

import json
import os
import time
import random

class ImitationLearning:
    def __init__(self, bot_folder):
        self.path = os.path.join(bot_folder, "imitation_data.json")
        if not os.path.exists(self.path):
            with open(self.path, "w") as f:
                json.dump([], f)

    def record(self, action, details):
        entry = {
            "timestamp": time.time(),
            "action": action,
            "details": details
        }

        try:
            with open(self.path, "r") as f:
                data = json.load(f)
        except:
            data = []

        data.append(entry)
        data = data[-5000:]

        with open(self.path, "w") as f:
            json.dump(data, f, indent=2)

    def sample(self):
        try:
            with open(self.path, "r") as f:
                data = json.load(f)
        except:
            return None

        if not data:
            return None

        return random.choice(data)

    # -----------------------------
    # MOVEMENT STYLE CLONING
    # -----------------------------
    def get_movement_style(self):
        try:
            with open(self.path, "r") as f:
                data = json.load(f)
        except:
            data = []

        if not data:
            # Default human-like movement
            return {
                "strafe_rate": 0.2,
                "jump_rate": 0.1,
                "zigzag_rate": 0.15,
                "camera_wiggle_rate": 0.3
            }

        counts = {
            "strafe": 0,
            "jump": 0,
            "zigzag": 0,
            "wiggle": 0
        }

        for entry in data:
            a = entry["action"]

            if "strafe" in a:
                counts["strafe"] += 1
            if "jump" in a:
                counts["jump"] += 1
            if "zigzag" in a:
                counts["zigzag"] += 1
            if "wiggle" in a or "camera" in a:
                counts["wiggle"] += 1

        total = max(1, len(data))

        return {
            "strafe_rate": counts["strafe"] / total,
            "jump_rate": counts["jump"] / total,
            "zigzag_rate": counts["zigzag"] / total,
            "camera_wiggle_rate": counts["wiggle"] / total
        }
