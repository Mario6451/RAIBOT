import tkinter as tk
from tkinter import ttk


class AIBehaviorTab(ttk.Frame):
    """
    AI Behavior Configuration Tab
    Replaces old training_tab.py
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
        title = ttk.Label(self, text="AI Behavior Settings", font=("Segoe UI", 14, "bold"))
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

        # Behavior mode
        mode_frame = ttk.LabelFrame(self, text="AI Mode")
        mode_frame.pack(fill="x", padx=10, pady=10)

        self.mode_var = tk.StringVar(value="wander")

        modes = ["wander", "follow", "chase", "sandbox"]
        for m in modes:
            ttk.Radiobutton(
                mode_frame,
                text=m.capitalize(),
                value=m,
                variable=self.mode_var,
                command=self._apply_mode
            ).pack(anchor="w", padx=10, pady=2)

        # Behavior sliders
        slider_frame = ttk.LabelFrame(self, text="Behavior Parameters")
        slider_frame.pack(fill="x", padx=10, pady=10)

        self.awareness_var = tk.DoubleVar(value=25.0)
        self.aggression_var = tk.DoubleVar(value=0.0)
        self.reaction_var = tk.DoubleVar(value=0.2)
        self.chat_freq_var = tk.DoubleVar(value=0.1)

        self._add_slider(slider_frame, "Awareness Radius", self.awareness_var, 5, 60, self._apply_behavior)
        self._add_slider(slider_frame, "Aggression", self.aggression_var, 0, 1, self._apply_behavior)
        self._add_slider(slider_frame, "Reaction Speed", self.reaction_var, 0.05, 1, self._apply_behavior)
        self._add_slider(slider_frame, "Chat Frequency", self.chat_freq_var, 0, 1, self._apply_behavior)

        # Personality
        personality_frame = ttk.LabelFrame(self, text="Personality")
        personality_frame.pack(fill="x", padx=10, pady=10)

        self.personality_var = tk.StringVar(value="neutral")

        personalities = ["neutral", "friendly", "aggressive", "playful"]
        for p in personalities:
            ttk.Radiobutton(
                personality_frame,
                text=p.capitalize(),
                value=p,
                variable=self.personality_var,
                command=self._apply_personality
            ).pack(anchor="w", padx=10, pady=2)

        # Status panel
        status_frame = ttk.LabelFrame(self, text="Current AI State")
        status_frame.pack(fill="x", padx=10, pady=10)

        self.status_labels = {
            "mode": ttk.Label(status_frame, text="Mode: -"),
            "awareness": ttk.Label(status_frame, text="Awareness: -"),
            "aggression": ttk.Label(status_frame, text="Aggression: -"),
            "reaction": ttk.Label(status_frame, text="Reaction Speed: -"),
            "chatfreq": ttk.Label(status_frame, text="Chat Frequency: -"),
            "personality": ttk.Label(status_frame, text="Personality: -"),
        }

        for lbl in self.status_labels.values():
            lbl.pack(anchor="w", padx=10, pady=2)

    # ---------------------------------------------------------
    # Helper: Add slider
    # ---------------------------------------------------------
    def _add_slider(self, parent, label, var, minv, maxv, cmd):
        frame = ttk.Frame(parent)
        frame.pack(fill="x", pady=5)

        ttk.Label(frame, text=label).pack(anchor="w", padx=10)

        slider = ttk.Scale(
            frame,
            from_=minv,
            to=maxv,
            orient="horizontal",
            variable=var,
            command=lambda e: cmd()
        )
        slider.pack(fill="x", padx=10)

    # ---------------------------------------------------------
    # Refresh bot list
    # ---------------------------------------------------------
    def _refresh_bot_list(self):
        bots = list(self.controller_ai.bots.keys())
        self.bot_dropdown["values"] = bots
        if bots:
            self.selected_bot.set(bots[0])

    # ---------------------------------------------------------
    # Apply mode
    # ---------------------------------------------------------
    def _apply_mode(self):
        bot = self.selected_bot.get()
        if bot in self.controller_ai.bots:
            runtime = self.controller_ai.bots[bot]
            runtime.brain.state.behavior.mode = self.mode_var.get()

    # ---------------------------------------------------------
    # Apply behavior sliders
    # ---------------------------------------------------------
    def _apply_behavior(self):
        bot = self.selected_bot.get()
        if bot in self.controller_ai.bots:
            b = self.controller_ai.bots[bot].brain.state.behavior
            b.awareness_radius = self.awareness_var.get()
            b.aggression = self.aggression_var.get()
            b.reaction_speed = self.reaction_var.get()
            b.chat_frequency = self.chat_freq_var.get()

    # ---------------------------------------------------------
    # Apply personality
    # ---------------------------------------------------------
    def _apply_personality(self):
        bot = self.selected_bot.get()
        if bot in self.controller_ai.bots:
            runtime = self.controller_ai.bots[bot]
            runtime.brain.state.behavior.personality = self.personality_var.get()

    # ---------------------------------------------------------
    # Status updater
    # ---------------------------------------------------------
    def _start_status_updater(self):
        self.after(500, self._update_status)

    def _update_status(self):
        bot = self.selected_bot.get()
        if bot in self.controller_ai.bots:
            b = self.controller_ai.bots[bot].brain.state.behavior

            self.status_labels["mode"].config(text=f"Mode: {b.mode}")
            self.status_labels["awareness"].config(text=f"Awareness: {b.awareness_radius}")
            self.status_labels["aggression"].config(text=f"Aggression: {b.aggression}")
            self.status_labels["reaction"].config(text=f"Reaction Speed: {b.reaction_speed}")
            self.status_labels["chatfreq"].config(text=f"Chat Frequency: {b.chat_frequency}")
            self.status_labels["personality"].config(text=f"Personality: {getattr(b, 'personality', 'neutral')}")

        self._start_status_updater()
