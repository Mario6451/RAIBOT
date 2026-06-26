import tkinter as tk
from tkinter import ttk

class AITab(ttk.Frame):
    """
    AI Control Tab
    - start/stop bots
    - change AI mode
    - view AI state
    """

    def __init__(self, parent, controller_ai, controller_bots):
        super().__init__(parent)

        self.controller_ai = controller_ai
        self.controller_bots = controller_bots

        self._build_ui()
        self._start_status_updater()

    # ---------------------------------------------------------
    # UI Layout
    # ---------------------------------------------------------
    def _build_ui(self):
        # Title
        title = ttk.Label(self, text="AI Control", font=("Segoe UI", 14, "bold"))
        title.pack(pady=10)

        # Bot selection
        bot_frame = ttk.Frame(self)
        bot_frame.pack(pady=5)

        ttk.Label(bot_frame, text="Select Bot:").pack(side="left", padx=5)

        self.bot_var = tk.StringVar()
        self.bot_dropdown = ttk.Combobox(
            bot_frame,
            textvariable=self.bot_var,
            state="readonly",
            width=20
        )
        self.bot_dropdown.pack(side="left", padx=5)

        self._refresh_bot_list()

        # Start/Stop buttons
        btn_frame = ttk.Frame(self)
        btn_frame.pack(pady=10)

        self.start_btn = ttk.Button(btn_frame, text="Start AI", command=self._start_ai)
        self.start_btn.pack(side="left", padx=5)

        self.stop_btn = ttk.Button(btn_frame, text="Stop AI", command=self._stop_ai)
        self.stop_btn.pack(side="left", padx=5)

        # Mode selector
        mode_frame = ttk.LabelFrame(self, text="AI Mode")
        mode_frame.pack(pady=10, fill="x", padx=10)

        self.mode_var = tk.StringVar(value="wander")

        modes = ["wander", "follow", "chase", "sandbox"]
        for m in modes:
            ttk.Radiobutton(
                mode_frame,
                text=m.capitalize(),
                value=m,
                variable=self.mode_var,
                command=self._change_mode
            ).pack(anchor="w", padx=10, pady=2)

        # Status panel
        status_frame = ttk.LabelFrame(self, text="AI Status")
        status_frame.pack(pady=10, fill="x", padx=10)

        self.status_labels = {
            "running": ttk.Label(status_frame, text="Running: -"),
            "mode": ttk.Label(status_frame, text="Mode: -"),
            "yaw": ttk.Label(status_frame, text="Yaw: -"),
            "stuck": ttk.Label(status_frame, text="Stuck: -"),
            "target": ttk.Label(status_frame, text="Target: -"),
        }

        for lbl in self.status_labels.values():
            lbl.pack(anchor="w", padx=10, pady=2)

        # Refresh button
        ttk.Button(self, text="Refresh Bots", command=self._refresh_bot_list).pack(pady=10)

    # ---------------------------------------------------------
    # Bot list refresh
    # ---------------------------------------------------------
    def _refresh_bot_list(self):
        bots = self.controller_bots.get_bot_names()
        self.bot_dropdown["values"] = bots
        if bots:
            self.bot_var.set(bots[0])

    # ---------------------------------------------------------
    # Start AI
    # ---------------------------------------------------------
    def _start_ai(self):
        bot_name = self.bot_var.get()
        if not bot_name:
            return

        cfg = self.controller_bots.get_bot_config(bot_name)
        if not cfg:
            print("[AI Tab] No config for bot:", bot_name)
            return

        self.controller_ai.start_bot(cfg)

    # ---------------------------------------------------------
    # Stop AI
    # ---------------------------------------------------------
    def _stop_ai(self):
        bot_name = self.bot_var.get()
        if bot_name:
            self.controller_ai.stop_bot(bot_name)

    # ---------------------------------------------------------
    # Change AI mode
    # ---------------------------------------------------------
    def _change_mode(self):
        bot_name = self.bot_var.get()
        mode = self.mode_var.get()

        if bot_name in self.controller_ai.bots:
            runtime = self.controller_ai.bots[bot_name]
            runtime.brain.state.behavior.mode = mode

    # ---------------------------------------------------------
    # Status updater loop
    # ---------------------------------------------------------
    def _start_status_updater(self):
        self.after(500, self._update_status)

    def _update_status(self):
        bot_name = self.bot_var.get()
        if bot_name in self.controller_ai.bots:
            status = self.controller_ai.get_status().get(bot_name, {})

            self.status_labels["running"].config(text=f"Running: {status.get('running', False)}")
            self.status_labels["mode"].config(text=f"Mode: {status.get('mode', '-')}")
            self.status_labels["yaw"].config(text=f"Yaw: {round(status.get('yaw', 0), 2)}")
            self.status_labels["stuck"].config(text=f"Stuck: {status.get('stuck', False)}")
            self.status_labels["target"].config(text=f"Target: {status.get('target', None)}")

        self._start_status_updater()
