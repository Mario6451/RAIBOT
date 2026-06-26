import tkinter as tk
from tkinter import ttk
import time


class AIProfilerTab(ttk.Frame):
    """
    AI Performance Profiler
    - timing per subsystem
    """

    def __init__(self, parent, controller_ai):
        super().__init__(parent)

        self.controller_ai = controller_ai
        self.selected_bot = tk.StringVar()

        self._build_ui()
        self._start_updater()

    def _build_ui(self):
        title = ttk.Label(self, text="AI Performance Profiler", font=("Segoe UI", 14, "bold"))
        title.pack(pady=10)

        bot_frame = ttk.Frame(self)
        bot_frame.pack(pady=5)

        ttk.Label(bot_frame, text="Bot:").pack(side="left", padx=5)

        self.bot_dropdown = ttk.Combobox(
            bot_frame,
            textvariable=self.selected_bot,
            state="readonly",
            width=20
        )
        self.bot_dropdown.pack(side="left", padx=5)

        ttk.Button(bot_frame, text="Refresh", command=self._refresh_bot_list).pack(side="left", padx=5)

        # Metrics
        metrics_frame = ttk.LabelFrame(self, text="Timing Metrics")
        metrics_frame.pack(fill="x", padx=10, pady=10)

        self.labels = {
            "tick_time": ttk.Label(metrics_frame, text="Tick Time: -"),
            "perception_time": ttk.Label(metrics_frame, text="Perception Time: -"),
            "pathfinding_time": ttk.Label(metrics_frame, text="Pathfinding Time: -"),
            "behavior_time": ttk.Label(metrics_frame, text="Behavior Time: -"),
            "movement_time": ttk.Label(metrics_frame, text="Movement Time: -"),
        }

        for lbl in self.labels.values():
            lbl.pack(anchor="w", padx=10, pady=2)

    def _refresh_bot_list(self):
        bots = list(self.controller_ai.bots.keys())
        self.bot_dropdown["values"] = bots
        if bots:
            self.selected_bot.set(bots[0])

    def _start_updater(self):
        self.after(500, self._update)

    def _update(self):
        bot = self.selected_bot.get()
        rt = self.controller_ai.bots.get(bot)
        if rt:
            prof = getattr(rt.brain, "profiler", None)
            if prof:
                self.labels["tick_time"].config(text=f"Tick Time: {prof.tick_time:.4f}s")
                self.labels["perception_time"].config(text=f"Perception Time: {prof.perception_time:.4f}s")
                self.labels["pathfinding_time"].config(text=f"Pathfinding Time: {prof.pathfinding_time:.4f}s")
                self.labels["behavior_time"].config(text=f"Behavior Time: {prof.behavior_time:.4f}s")
                self.labels["movement_time"].config(text=f"Movement Time: {prof.movement_time:.4f}s")

        self._start_updater()
