import tkinter as tk
from tkinter import ttk


class BotManagerTab(ttk.Frame):
    """
    Bot Manager
    - table of bots
    - start/stop/restart
    """

    def __init__(self, parent, controller_ai, controller_bots):
        super().__init__(parent)

        self.controller_ai = controller_ai
        self.controller_bots = controller_bots

        self._build_ui()
        self._start_updater()

    def _build_ui(self):
        title = ttk.Label(self, text="Bot Manager", font=("Segoe UI", 14, "bold"))
        title.pack(pady=10)

        # Treeview
        columns = ("status", "mode", "x", "z", "target")
        self.tree = ttk.Treeview(self, columns=columns, show="headings", height=15)
        for col in columns:
            self.tree.heading(col, text=col.capitalize())
            self.tree.column(col, width=100)

        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        # Buttons
        btn_frame = ttk.Frame(self)
        btn_frame.pack(pady=5)

        ttk.Button(btn_frame, text="Refresh", command=self._refresh).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Start Selected", command=self._start_selected).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Stop Selected", command=self._stop_selected).pack(side="left", padx=5)

    def _refresh(self):
        self.tree.delete(*self.tree.get_children())

        status = self.controller_ai.get_status()
        for name, s in status.items():
            self.tree.insert(
                "",
                "end",
                iid=name,
                values=(
                    "running" if s.get("running") else "stopped",
                    s.get("mode", "-"),
                    round(s.get("x", 0), 2),
                    round(s.get("y", 0), 2),
                    s.get("target", "-"),
                )
            )

    def _start_selected(self):
        sel = self.tree.selection()
        for bot in sel:
            cfg = self.controller_bots.get_bot_config(bot)
            if cfg:
                self.controller_ai.start_bot(cfg)

    def _stop_selected(self):
        sel = self.tree.selection()
        for bot in sel:
            self.controller_ai.stop_bot(bot)

    def _start_updater(self):
        self.after(1000, self._tick)

    def _tick(self):
        self._refresh()
        self._start_updater()
