# training/memory.py

import json
import os
import time

class TrainingMemory:
    def __init__(self, bot_folder):
        self.path = os.path.join(bot_folder, "training_memory.json")
        if not os.path.exists(self.path):
            with open(self.path, "w") as f:
                json.dump([], f)

        # New safe-max memory size
        self.MAX_MEMORY = 131072  # 128K entries

    def log(self, entry):
        entry["timestamp"] = time.time()

        try:
            with open(self.path, "r") as f:
                data = json.load(f)
        except:
            data = []

        data.append(entry)

        # Keep last 128K entries
        data = data[-self.MAX_MEMORY:]

        with open(self.path, "w") as f:
            json.dump(data, f, indent=2)
