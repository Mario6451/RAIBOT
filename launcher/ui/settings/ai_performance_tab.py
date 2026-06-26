import tkinter as tk
from tkinter import ttk
import time


class AIPerformanceTab(ttk.Frame):
    """
    AI Performance Metrics Tab
    Replaces old training_stats_tab.py
    """

    def __init__(self, parent, controller_ai):
        super().__init__(parent)

        self.controller_ai = controller_ai
        self.selected_bot = tk.StringVar()

        self._build_ui()
        self._start_status_updater()

    # ---------------------------------------------------------
    # UI Layout
    # ---------------------------------------------------------
    def _build_ui(self):
        title = ttk.Label(self, text="AI Performance Metrics", font=("Segoe UI", 14, "bold"))
        title.pack(pady=10)

        # Bot selector
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

        self._refresh_bot_list()

        # Metrics panel
        metrics_frame = ttk.LabelFrame(self, text="Live Metrics")
        metrics_frame.pack(fill="x", padx=10, pady=10)

        self.labels = {
            "perception_rate": ttk.Label(metrics_frame, text="Perception Rate: -"),
            "last_perception": ttk.Label(metrics_frame, text="Last Perception Update: -"),
            "reaction_time": ttk.Label(metrics_frame, text="Reaction Time: -"),
            "stuck": ttk.Label(metrics_frame, text="Stuck: -"),
            "stuck_counter": ttk.Label(metrics_frame, text="Stuck Count: -"),
            "visited_points": ttk.Label(metrics_frame, text="Visited Points: -"),
            "stuck_points": ttk.Label(metrics_frame, text="Stuck Points: -"),
            "last_stuck": ttk.Label(metrics_frame, text="Last Stuck Time: -"),
            "yaw": ttk.Label(metrics_frame, text="Camera Yaw: -"),
            "mode": ttk.Label(metrics_frame, text="Mode: -"),
        }

        for lbl in self.labels.values():
            lbl.pack(anchor="w", padx=10, pady=2)

        # Navigation memory panel
        nav_frame = ttk.LabelFrame(self, text="Navigation Memory")
        nav_frame.pack(fill="x", padx=10, pady=10)

        self.nav_labels = {
            "last_path_len": ttk.Label(nav_frame, text="Last Path Length: -"),
            "nav_memory_size": ttk.Label(nav_frame, text="Navigation Memory Size: -"),
        }

        for lbl in self.nav_labels.values():
            lbl.pack(anchor="w", padx=10, pady=2)

    # ---------------------------------------------------------
    # Refresh bot list
    # ---------------------------------------------------------
    def _refresh_bot_list(self):
        bots = list(self.controller_ai.bots.keys())
        self.bot_dropdown["values"] = bots
        if bots:
            self.selected_bot.set(bots[0])

    # ---------------------------------------------------------
    # Status updater loop
    # ---------------------------------------------------------
    def _start_status_updater(self):
        self.after(500, self._update_status)

    def _update_status(self):
        bot = self.selected_bot.get()
        if bot in self.controller_ai.bots:
            runtime = self.controller_ai.bots[bot]
            state = runtime.brain.state

            # Perception timing
            now = time.time()
            perception_delay = now - state.last_perception_update
            perception_rate = round(1 / perception_delay, 2) if perception_delay > 0 else 0

            # Update metrics
            self.labels["perception_rate"].config(text=f"Perception Rate: {perception_rate} Hz")
            self.labels["last_perception"].config(text=f"Last Perception Update: {round(perception_delay, 3)}s ago")
            self.labels["reaction_time"].config(text=f"Reaction Time: {state.behavior.reaction_speed}s")
            self.labels["stuck"].config(text=f"Stuck: {state.stuck}")
            self.labels["stuck_counter"].config(text=f"Stuck Count: {state.stuck_counter}")
            self.labels["visited_points"].config(text=f"Visited Points: {len(state.nav.visited_points)}")
            self.labels["stuck_points"].config(text=f"Stuck Points: {len(state.nav.stuck_points)}")

            last_stuck = (
                f"{round(now - state.nav.last_stuck_time, 2)}s ago"
                if state.nav.last_stuck_time > 0 else "-"
            )
            self.labels["last_stuck"].config(text=f"Last Stuck Time: {last_stuck}")

            self.labels["yaw"].config(text=f"Camera Yaw: {round(state.camera.yaw, 2)}°")
            self.labels["mode"].config(text=f"Mode: {state.behavior.mode}")

            # Navigation memory
            self.nav_labels["last_path_len"].config(
                text=f"Last Path Length: {len(state.nav.last_path)}"
            )
            self.nav_labels["nav_memory_size"].config(
                text=f"Navigation Memory Size: {len(state.nav.visited_points)}"
            )

        self._start_status_updater()
