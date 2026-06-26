import tkinter as tk
from tkinter import ttk

class BotsTab(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        ttk.Label(self, text="New Bot Name:").grid(row=0, column=0, sticky="w")
        self.new_bot_name = tk.StringVar()
        ttk.Entry(self, textvariable=self.new_bot_name).grid(row=0, column=1, sticky="ew")
        ttk.Button(self, text="Create Bot", command=self.controller.create_bot).grid(row=0, column=2)

        self.status_var = tk.StringVar()
        ttk.Label(self, textvariable=self.status_var).grid(row=1, column=0, columnspan=3, sticky="w")

        self.columnconfigure(1, weight=1)

    def show_status(self, text):
        self.status_var.set(text)
