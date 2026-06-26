# training/instruction.py

import json
import os

class InstructionLearning:
    def __init__(self, bot_folder):
        self.path = os.path.join(bot_folder, "knowledge.json")
        if not os.path.exists(self.path):
            with open(self.path, "w") as f:
                json.dump({}, f)

    def teach(self, key, value):
        try:
            with open(self.path, "r") as f:
                data = json.load(f)
        except:
            data = {}

        data[key] = value

        with open(self.path, "w") as f:
            json.dump(data, f, indent=2)

    def get(self, key):
        try:
            with open(self.path, "r") as f:
                data = json.load(f)
        except:
            return None

        return data.get(key)
