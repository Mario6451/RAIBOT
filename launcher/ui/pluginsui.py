import tkinter as tk
from tkinter import ttk
from core.plugins import PLUGINS

class PluginsUI(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        for plugin in PLUGINS:
            var = tk.BooleanVar(value=plugin.enabled)
            ttk.Checkbutton(self, text=plugin.name, variable=var).pack(anchor="w")
