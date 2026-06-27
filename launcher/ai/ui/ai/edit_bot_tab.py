# ai/ui/edit_bot_tab.py

import tkinter as tk
from tkinter import ttk

class EditBotTab(ttk.Frame):
    def __init__(self, parent, panel):
        super().__init__(parent)
        self.panel = panel

        # Title
        ttk.Label(self, text="Edit Bot", font=("Segoe UI", 14, "bold")).pack(pady=10)

        # Bot selector
        ttk.Label(self, text="Select Bot:").pack()
        self.bot_var = tk.StringVar()
        self.bot_dropdown = ttk.Combobox(self, textvariable=self.bot_var, state="readonly")
        self.bot_dropdown.pack(pady=5)

        # Personality selector
        ttk.Label(self, text="Select Personality:").pack()
        self.personality_var = tk.StringVar()
        self.personality_dropdown = ttk.Combobox(self, textvariable=self.personality_var, state="readonly")
        self.personality_dropdown.pack(pady=5)

        # Assign button
        ttk.Button(self, text="Assign Personality", command=self.assign_personality).pack(pady=10)

        # Lock toggle
        self.lock_var = tk.BooleanVar()
        ttk.Checkbutton(self, text="Lock Personality", variable=self.lock_var, command=self.toggle_lock).pack()

        # Load initial data
        self.refresh()

    def refresh(self):
        # Load bots
        bots = self.panel.list_bots()
        bot_names = [bot.name for bot in bots]
        self.bot_dropdown["values"] = bot_names

        # Load personalities
        personalities = self.panel.list_personalities()
        self.personality_dropdown["values"] = [f"{pid}: {name}" for pid, name in personalities]

    def assign_personality(self):
        bot_name = self.bot_var.get()
        personality_text = self.personality_var.get()

        if not bot_name or not personality_text:
            return

        pid = int(personality_text.split(":")[0])

        # Find bot object
        for bot in self.panel.list_bots():
            if bot.name == bot_name:
                self.panel.select_bot(bot)
                self.panel.assign_personality(pid)
                break

    def toggle_lock(self):
        bot_name = self.bot_var.get()
        for bot in self.panel.list_bots():
            if bot.name == bot_name:
                bot.lock_personality = self.lock_var.get()
                break
