# ai/ui/live_bot_window.py

import tkinter as tk
from tkinter import ttk
import math

class LiveBotWindow(tk.Toplevel):
    def __init__(self, parent, controller_ai, on_select=None, refresh_ms=500):
        super().__init__(parent)

        self.title("Live Bot Monitor")
        self.geometry("900x600")
        self.controller_ai = controller_ai
        self.on_select = on_select
        self.refresh_ms = refresh_ms

        # Layout: left = bot list, right = minimap
        container = ttk.Frame(self)
        container.pack(fill="both", expand=True)

        # LEFT SIDE: BOT LIST
        left = ttk.Frame(container)
        left.pack(side="left", fill="y", padx=10, pady=10)

        ttk.Label(left, text="Live Bot List", font=("Segoe UI", 12, "bold")).pack(pady=5)

        columns = ("name", "personality", "mode", "threat", "pos")
        self.tree = ttk.Treeview(left, columns=columns, show="headings", height=25)

        for col, text in zip(columns, ["Bot", "Personality", "Mode", "Threat", "Position"]):
            self.tree.heading(col, text=text)
            self.tree.column(col, width=120)

        self.tree.pack(fill="y", expand=False)
        self.tree.bind("<<TreeviewSelect>>", self._on_select)

        # RIGHT SIDE: MINIMAP
        right = ttk.Frame(container)
        right.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        ttk.Label(right, text="Mini‑Map Preview", font=("Segoe UI", 12, "bold")).pack(pady=5)

        self.canvas = tk.Canvas(right, bg="#1e1e1e")
        self.canvas.pack(fill="both", expand=True)

        # Start auto-refresh
        self.refresh()

    # ---------------------------------------------------------
    # AUTO REFRESH
    # ---------------------------------------------------------
    def refresh(self):
        self._refresh_bot_list()
        self._refresh_minimap()

        if self.winfo_exists():
            self.after(self.refresh_ms, self.refresh)

    # ---------------------------------------------------------
    # BOT LIST
    # ---------------------------------------------------------
    def _refresh_bot_list(self):
        self.tree.delete(*self.tree.get_children())

        for bot in self.controller_ai.world.bots:
            personality = getattr(bot, "personality_id", "None")
            mode = getattr(bot, "mode", "idle")
            threat = self.controller_ai.threat.threat_level(bot)
            pos = f"({int(bot.x)}, {int(bot.z)})"

            self.tree.insert("", "end", iid=bot.name, values=(
                bot.name, personality, mode, threat, pos
            ))

    # ---------------------------------------------------------
    # MINIMAP RENDERING
    # ---------------------------------------------------------
    def _refresh_minimap(self):
        self.canvas.delete("all")

        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()

        if w < 10 or h < 10:
            return

        # World bounds (you can adjust these)
        WORLD_SIZE = 1024

        def world_to_canvas(x, z):
            cx = (x / WORLD_SIZE) * w
            cy = (z / WORLD_SIZE) * h
            return cx, cy

        # Draw bots
        for bot in self.controller_ai.world.bots:
            cx, cy = world_to_canvas(bot.x, bot.z)
            self.canvas.create_oval(cx-4, cy-4, cx+4, cy+4, fill="cyan")

        # Draw players
        for player in self.controller_ai.world.players:
            cx, cy = world_to_canvas(player.x, player.z)
            self.canvas.create_oval(cx-6, cy-6, cx+6, cy+6, fill="yellow")

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

        for bot in self.controller_ai.world.bots:
            if bot.name == bot_name:
                self.on_select(bot)
                break
