import tkinter as tk
from tkinter import ttk


class AICommandTab(ttk.Frame):
    """
    AI Command Tab
    - select bot
    - issue commands (move, follow, stop, reset)
    - send chat as bot
    """

    def __init__(self, parent, controller_ai, controller_bots):
        super().__init__(parent)

        self.controller_ai = controller_ai
        self.controller_bots = controller_bots
        self.selected_bot = tk.StringVar()

        self._build_ui()
        self._refresh_bot_list()

    def _build_ui(self):
        title = ttk.Label(self, text="AI Command Center", font=("Segoe UI", 14, "bold"))
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

        ttk.Button(bot_frame, text="Refresh", command=self._refresh_bot_list).pack(side="left", padx=5)

        # Command buttons
        cmd_frame = ttk.LabelFrame(self, text="Commands")
        cmd_frame.pack(fill="x", padx=10, pady=10)

        ttk.Button(cmd_frame, text="Start", command=self._cmd_start).pack(side="left", padx=5, pady=5)
        ttk.Button(cmd_frame, text="Stop", command=self._cmd_stop).pack(side="left", padx=5, pady=5)
        ttk.Button(cmd_frame, text="Reset", command=self._cmd_reset).pack(side="left", padx=5, pady=5)

        ttk.Button(cmd_frame, text="Follow Target", command=self._cmd_follow).pack(side="left", padx=5, pady=5)
        ttk.Button(cmd_frame, text="Wander", command=self._cmd_wander).pack(side="left", padx=5, pady=5)
        ttk.Button(cmd_frame, text="Sandbox", command=self._cmd_sandbox).pack(side="left", padx=5, pady=5)

        # Move to position
        move_frame = ttk.LabelFrame(self, text="Move To Position")
        move_frame.pack(fill="x", padx=10, pady=10)

        self.move_x = tk.DoubleVar(value=0.0)
        self.move_z = tk.DoubleVar(value=0.0)

        ttk.Label(move_frame, text="X:").pack(side="left", padx=5)
        ttk.Entry(move_frame, textvariable=self.move_x, width=10).pack(side="left", padx=5)

        ttk.Label(move_frame, text="Z:").pack(side="left", padx=5)
        ttk.Entry(move_frame, textvariable=self.move_z, width=10).pack(side="left", padx=5)

        ttk.Button(move_frame, text="Send Move Command", command=self._cmd_move_to).pack(side="left", padx=10)

        # Chat
        chat_frame = ttk.LabelFrame(self, text="Chat as Bot")
        chat_frame.pack(fill="x", padx=10, pady=10)

        self.chat_entry = ttk.Entry(chat_frame, width=60)
        self.chat_entry.pack(side="left", padx=5)

        ttk.Button(chat_frame, text="Send", command=self._cmd_chat).pack(side="left", padx=5)

    def _refresh_bot_list(self):
        bots = list(self.controller_ai.bots.keys())
        self.bot_dropdown["values"] = bots
        if bots:
            self.selected_bot.set(bots[0])

    def _get_runtime(self):
        bot = self.selected_bot.get()
        return self.controller_ai.bots.get(bot)

    def _cmd_start(self):
        bot = self.selected_bot.get()
        cfg = self.controller_bots.get_bot_config(bot)
        if cfg:
            self.controller_ai.start_bot(cfg)

    def _cmd_stop(self):
        bot = self.selected_bot.get()
        self.controller_ai.stop_bot(bot)

    def _cmd_reset(self):
        rt = self._get_runtime()
        if rt:
            rt.brain.reset()

    def _cmd_follow(self):
        rt = self._get_runtime()
        if rt:
            rt.brain.state.behavior.mode = "follow"

    def _cmd_wander(self):
        rt = self._get_runtime()
        if rt:
            rt.brain.state.behavior.mode = "wander"

    def _cmd_sandbox(self):
        rt = self._get_runtime()
        if rt:
            rt.brain.state.behavior.mode = "sandbox"

    def _cmd_move_to(self):
        rt = self._get_runtime()
        if rt:
            x = self.move_x.get()
            z = self.move_z.get()
            rt.brain.command_move_to(x, z)

    def _cmd_chat(self):
        rt = self._get_runtime()
        msg = self.chat_entry.get().strip()
        if rt and msg:
            rt.brain.command_chat(msg)
            self.chat_entry.delete(0, "end")
