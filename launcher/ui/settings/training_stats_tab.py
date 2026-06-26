# ui/settings/training_stats_tab.py

import tkinter as tk
from tkinter import ttk, filedialog
import json
import os

class TrainingStatsTab:
    def __init__(self, parent):
        self.frame = ttk.Frame(parent)
        self.build()

    def build(self):
        frame = ttk.LabelFrame(self.frame, text="AI Skill Levels")
        frame.pack(fill="x", padx=10, pady=10)

        # Movement
        ttk.Label(frame, text="Movement Skill:").pack(anchor="w")
        self.movement_bar = ttk.Progressbar(frame, length=300, maximum=10)
        self.movement_bar.pack(pady=3)

        # Awareness
        ttk.Label(frame, text="Awareness Skill:").pack(anchor="w")
        self.awareness_bar = ttk.Progressbar(frame, length=300, maximum=10)
        self.awareness_bar.pack(pady=3)

        # Social
        ttk.Label(frame, text="Social Skill:").pack(anchor="w")
        self.social_bar = ttk.Progressbar(frame, length=300, maximum=10)
        self.social_bar.pack(pady=3)

        # Tools
        ttk.Label(frame, text="Tools Skill:").pack(anchor="w")
        self.tools_bar = ttk.Progressbar(frame, length=300, maximum=10)
        self.tools_bar.pack(pady=3)

        # Buttons
        ttk.Button(frame, text="Refresh Stats", command=self.refresh).pack(pady=5)
        ttk.Button(frame, text="Reset Training", command=self.reset).pack(pady=5)
        ttk.Button(frame, text="Export Training Profile", command=self.export).pack(pady=5)
        ttk.Button(frame, text="Import Training Profile", command=self.import_profile).pack(pady=5)

    # ------------------- Backend Logic -------------------

    def _stats_path(self):
        return os.path.join("bot", "training", "skillstats.json")

    def refresh(self):
        try:
            with open(self._stats_path(), "r") as f:
                stats = json.load(f)

            self.movement_bar["value"] = stats.get("movement", 1)
            self.awareness_bar["value"] = stats.get("awareness", 1)
            self.social_bar["value"] = stats.get("social", 1)
            self.tools_bar["value"] = stats.get("tools", 1)

        except Exception as e:
            print(f"[TrainingStats] Failed to refresh: {e}")

    def reset(self):
        data = {"movement": 1, "awareness": 1, "social": 1, "tools": 1}
        try:
            with open(self._stats_path(), "w") as f:
                json.dump(data, f, indent=2)
            print("[TrainingStats] Reset complete.")
            self.refresh()
        except Exception as e:
            print(f"[TrainingStats] Reset failed: {e}")

    def export(self):
        path = filedialog.asksaveasfilename(defaultextension=".json")
        if not path:
            return

        try:
            with open(self._stats_path(), "r") as f:
                data = json.load(f)
            with open(path, "w") as f:
                json.dump(data, f, indent=2)
            print("[TrainingStats] Exported.")
        except Exception as e:
            print(f"[TrainingStats] Export failed: {e}")

    def import_profile(self):
        path = filedialog.askopenfilename()
        if not path:
            return

        try:
            with open(path, "r") as f:
                data = json.load(f)
            with open(self._stats_path(), "w") as f:
                json.dump(data, f, indent=2)
            print("[TrainingStats] Imported.")
            self.refresh()
        except Exception as e:
            print(f"[TrainingStats] Import failed: {e}")
