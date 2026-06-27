# ai/ui/live_bot_list.py

import tkinter as tk
from tkinter import ttk

class LiveBotList(ttk.Frame):
    def __init__(self, parent, controller_ai, on_select=None, refresh_ms=500):
        super().__init__(parent)

        self.controller_ai = controller_ai
        self.on_select = on_select
        self.refresh_ms = refresh_ms

        # Title
        ttk.Label(self, text="Live Bot List", font=("Segoe UI", 12, "bold")).pack(pady=5)

        # Treeview
        columns = ("name", "personality", "mode", "threat", "pos")
        self.tree = ttk.Treeview(self, columns=columns, show="headings", height=15)

        self.tree.heading("name", text="Bot")
        self.tree.heading("personality", text="Personality")
        self.tree.heading("mode", text="Mode")
        self.tree.heading("threat", text="Threat")
        self.tree.heading("pos", text="Position")

        self.tree.column("name", width=120)
        self.tree.column("personality", width=150)
        self.tree.column("mode", width=100)
        self.tree.column("threat", width=60)
        self.tree.column("pos", width=120)

        self.tree.pack(fill="both", expand=True)

        # Bind selection
        self.tree.bind("<<TreeviewSelect>>", self._on_select)

        # Start auto-refresh
        self.refresh()

    # ---------------------------------------------------------
    # AUTO REFRESH
    # ---------------------------------------------------------
    def refresh(self):
        self.tree.delete(*self.tree.get_children())

        for bot in self.controller_ai.world.bots:
            personality = getattr(bot, "personality_id", "None")
            mode = getattr(bot, "mode", "idle")
            threat = self.controller_ai.threat.threat_level(bot)
            pos = f"({int(bot.x)}, {int(bot.z)})"

            self.tree.insert("", "end", iid=bot.name, values=(
                bot.name,
                personality,
                mode,
                threat,
                pos
            ))

        self.after(self.refresh_ms, self.refresh)

    # ---------------------------------------------------------
    # SELECTION CALLBACK
    # ---------------------------------------------------------
    def _on_select(self, event):
        if not self.on_select:
            return

        selected = self.tree.selection()
        if not selected:
            return

        bot_name = selected[0]

        # Find bot object
        for bot in self.controller_ai.world.bots:
            if bot.name == bot_name:
                self.on_select(bot)
                break
