import tkinter as tk
from tkinter import ttk, filedialog
from core.settings import SETTINGS, save_settings

class ExePicker(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        ttk.Label(self, text="Roblox Executable:").pack(anchor="w")
        self.entry = ttk.Entry(self)
        self.entry.insert(0, SETTINGS["default_exe"])
        self.entry.pack(fill="x")

        ttk.Button(self, text="Browse", command=self.pick).pack(pady=5)
        ttk.Button(self, text="Save", command=self.save).pack()

    def pick(self):
        path = filedialog.askopenfilename(filetypes=[("Executable", "*.exe")])
        if path:
            self.entry.delete(0, "end")
            self.entry.insert(0, path)

    def save(self):
        SETTINGS["default_exe"] = self.entry.get()
        save_settings(SETTINGS)
