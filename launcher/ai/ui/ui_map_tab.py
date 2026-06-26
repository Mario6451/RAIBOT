# launcher/ui/ui_map_tab.py

import tkinter as tk
from tkinter import ttk
import math


def build_map_tab(ui):
    frame = ui.map_tab

    left = ttk.Frame(frame)
    left.pack(side="left", fill="both", expand=True, padx=10, pady=10)

    right = ttk.Frame(frame)
    right.pack(side="right", fill="both", expand=True, padx=10, pady=10)

    ttk.Label(left, text="🗺 Top‑Down Map", font=("Segoe UI", 14, "bold")).pack(pady=5)
    ui.map_canvas = tk.Canvas(left, width=500, height=500, bg="#1a1a1a")
    ui.map_canvas.pack()

    ui.map_tooltip = ttk.Label(left, text="", font=("Segoe UI", 9),
                               foreground="white", background="#333")
    ui.map_tooltip.place_forget()
    ui._bot_markers = []

    ttk.Label(right, text="🎥 Vision Preview", font=("Segoe UI", 14, "bold")).pack(pady=5)
    ui.preview_label = ttk.Label(right, text="(no frame)")
    ui.preview_label.pack(fill="both", expand=True)

    def update_map(bots, players):
        ui.map_canvas.delete("all")
        ui._bot_markers = []

        for i in range(0, 500, 50):
            ui.map_canvas.create_line(i, 0, i, 500, fill="#333")
            ui.map_canvas.create_line(0, i, 500, i, fill="#333")

        for x, y, angle, name in bots:
            ui.map_canvas.create_oval(x-5, y-5, x+5, y+5, fill="lime")
            dx = 15 * math.cos(math.radians(angle))
            dy = 15 * math.sin(math.radians(angle))
            ui.map_canvas.create_line(x, y, x+dx, y+dy, fill="white", width=2)
            ui._bot_markers.append((x, y, name))

        for x, y in players:
            ui.map_canvas.create_oval(x-5, y-5, x+5, y+5, fill="cyan")

    def _on_map_hover(event):
        x, y = event.x, event.y
        for bx, by, name in ui._bot_markers:
            if abs(bx - x) <= 6 and abs(by - y) <= 6:
                ui.map_tooltip.config(text=name)
                ui.map_tooltip.place(x=x+10, y=y+10)
                return
        ui.map_tooltip.place_forget()

    ui.map_canvas.bind("<Motion>", _on_map_hover)

    def update_preview_text(text):
        ui.preview_label.config(text=text)

    ui.update_map = update_map
    ui.update_preview_text = update_preview_text
