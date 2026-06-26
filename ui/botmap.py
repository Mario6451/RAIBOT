import tkinter as tk
from tkinter import ttk
from core.botmanager import BOT_MANAGER

class BotMap(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.canvas = tk.Canvas(self, bg="black")
        self.canvas.pack(fill="both", expand=True)

        self.update_map()

    def update_map(self):
        self.canvas.delete("all")

        for bot in BOT_MANAGER.bots:
            x = bot.x
            y = bot.y
            self.canvas.create_oval(x-5, y-5, x+5, y+5, fill="lime")
            self.canvas.create_text(x, y-10, text=bot.name, fill="white")

        self.after(100, self.update_map)
