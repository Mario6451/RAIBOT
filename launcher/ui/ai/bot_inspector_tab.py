import tkinter as tk
from tkinter import ttk


class BotInspectorTab(ttk.Frame):
    """
    Bot Inspector
    - deep per-bot state
    - behavior, perception, nav, camera, target
    """

    def __init__(self, parent, controller_ai):
        super().__init__(parent)

        self.controller_ai = controller_ai
        self.selected_bot = tk.StringVar()

        self._build_ui()
        self._start_updater()

    def _build_ui(self):
        title = ttk.Label(self, text="Bot Inspector", font=("Segoe UI", 14, "bold"))
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

        # Sections
        self.behavior_frame = ttk.LabelFrame(self, text="Behavior")
        self.behavior_frame.pack(fill="x", padx=10, pady=5)

        self.perception_frame = ttk.LabelFrame(self, text="Perception")
        self.perception_frame.pack(fill="x", padx=10, pady=5)

        self.nav_frame = ttk.LabelFrame(self, text="Navigation")
        self.nav_frame.pack(fill="x", padx=10, pady=5)

        self.camera_frame = ttk.LabelFrame(self, text="Camera")
        self.camera_frame.pack(fill="x", padx=10, pady=5)

        self.target_frame = ttk.LabelFrame(self, text="Target")
        self.target_frame.pack(fill="x", padx=10, pady=5)

        # Labels
        self.behavior_labels = {
            "mode": ttk.Label(self.behavior_frame, text="Mode: -"),
            "aggression": ttk.Label(self.behavior_frame, text="Aggression: -"),
            "awareness": ttk.Label(self.behavior_frame, text="Awareness: -"),
            "reaction": ttk.Label(self.behavior_frame, text="Reaction Speed: -"),
        }

        self.perception_labels = {
            "last_update": ttk.Label(self.perception_frame, text="Last Perception: -"),
            "seen_players": ttk.Label(self.perception_frame, text="Seen Players: -"),
            "seen_obstacles": ttk.Label(self.perception_frame, text="Seen Obstacles: -"),
        }

        self.nav_labels = {
            "stuck": ttk.Label(self.nav_frame, text="Stuck: -"),
            "stuck_counter": ttk.Label(self.nav_frame, text="Stuck Counter: -"),
            "visited_points": ttk.Label(self.nav_frame, text="Visited Points: -"),
            "last_path_len": ttk.Label(self.nav_frame, text="Last Path Length: -"),
        }

        self.camera_labels = {
            "yaw": ttk.Label(self.camera_frame, text="Yaw: -"),
            "pitch": ttk.Label(self.camera_frame, text="Pitch: -"),
        }

        self.target_labels = {
            "target_player": ttk.Label(self.target_frame, text="Target Player: -"),
            "distance": ttk.Label(self.target_frame, text="Distance: -"),
        }

        for group in [
            self.behavior_labels,
            self.perception_labels,
            self.nav_labels,
            self.camera_labels,
            self.target_labels,
        ]:
            for lbl in group.values():
                lbl.pack(anchor="w", padx=10, pady=2)

    def _refresh_bot_list(self):
        bots = list(self.controller_ai.bots.keys())
        self.bot_dropdown["values"] = bots
        if bots:
            self.selected_bot.set(bots[0])

    def _start_updater(self):
        self.after(300, self._update)

    def _update(self):
        bot = self.selected_bot.get()
        rt = self.controller_ai.bots.get(bot)
        if rt:
            s = rt.brain.state

            # Behavior
            b = s.behavior
            self.behavior_labels["mode"].config(text=f"Mode: {b.mode}")
            self.behavior_labels["aggression"].config(text=f"Aggression: {b.aggression}")
            self.behavior_labels["awareness"].config(text=f"Awareness: {b.awareness_radius}")
            self.behavior_labels["reaction"].config(text=f"Reaction Speed: {b.reaction_speed}")

            # Perception
            p = s.perception
            self.perception_labels["last_update"].config(text=f"Last Perception: {s.last_perception_update}")
            self.perception_labels["seen_players"].config(text=f"Seen Players: {len(getattr(p, 'players', []))}")
            self.perception_labels["seen_obstacles"].config(text=f"Seen Obstacles: {len(getattr(p, 'obstacles', []))}")

            # Navigation
            n = s.nav
            self.nav_labels["stuck"].config(text=f"Stuck: {s.stuck}")
            self.nav_labels["stuck_counter"].config(text=f"Stuck Counter: {s.stuck_counter}")
            self.nav_labels["visited_points"].config(text=f"Visited Points: {len(n.visited_points)}")
            self.nav_labels["last_path_len"].config(text=f"Last Path Length: {len(n.last_path)}")

            # Camera
            c = s.camera
            self.camera_labels["yaw"].config(text=f"Yaw: {round(c.yaw, 2)}")
            self.camera_labels["pitch"].config(text=f"Pitch: {round(getattr(c, 'pitch', 0.0), 2)}")

            # Target
            t = s.target
            self.target_labels["target_player"].config(text=f"Target Player: {t.target_player}")
            self.target_labels["distance"].config(text=f"Distance: {round(getattr(t, 'distance', 0.0), 2)}")

        self._start_updater()
