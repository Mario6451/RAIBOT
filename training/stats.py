# training/stats.py

import json
import os

class SkillStats:
    def __init__(self, bot_folder):
        self.path = os.path.join(bot_folder, "skillstats.json")

        if os.path.exists(self.path):
            try:
                with open(self.path, "r") as f:
                    data = json.load(f)
                self.movement = data.get("movement", 1.0)
                self.awareness = data.get("awareness", 1.0)
                self.social = data.get("social", 1.0)
                self.tools = data.get("tools", 1.0)
            except:
                self._set_defaults()
        else:
            self._set_defaults()
            self._save()

    def _set_defaults(self):
        self.movement = 1.0
        self.awareness = 1.0
        self.social = 1.0
        self.tools = 1.0

    def _save(self):
        data = {
            "movement": self.movement,
            "awareness": self.awareness,
            "social": self.social,
            "tools": self.tools
        }
        with open(self.path, "w") as f:
            json.dump(data, f, indent=2)

    def apply_reward(self, reward):
        if reward > 0:
            self.movement += reward * 0.01
            self.awareness += reward * 0.005
            self.social += reward * 0.003
            self.tools += reward * 0.004
        else:
            self.movement += reward * 0.02

        self._save()
