# ui/settings/general_tab.py

import tkinter as tk
from tkinter import ttk

class GeneralTab:
    def __init__(self, parent, settings):
        self.settings = settings
        self.frame = ttk.Frame(parent)
        self.build()

    def build(self):
        frame = ttk.LabelFrame(self.frame, text="General Settings")
        frame.pack(fill="x", padx=10, pady=10)

        # Bot name
        ttk.Label(frame, text="Bot Name:").pack(anchor="w")
        self.bot_name_var = tk.StringVar(value=self.settings["general"]["bot_name"])
        ttk.Entry(frame, textvariable=self.bot_name_var).pack(fill="x", pady=3)

        # Model name
        ttk.Label(frame, text="Model Name:").pack(anchor="w")
        self.model_var = tk.StringVar(value=self.settings["general"]["model"])
        ttk.Entry(frame, textvariable=self.model_var).pack(fill="x", pady=3)

        # Model endpoint
        ttk.Label(frame, text="Model Endpoint:").pack(anchor="w")
        self.endpoint_var = tk.StringVar(value=self.settings["general"]["model_endpoint"])
        ttk.Entry(frame, textvariable=self.endpoint_var).pack(fill="x", pady=3)

        # Auto launch
        self.auto_launch_var = tk.BooleanVar(value=self.settings["general"]["auto_launch"])
        ttk.Checkbutton(
            frame,
            text="Auto-launch bot on start",
            variable=self.auto_launch_var
        ).pack(anchor="w", pady=3)

        # EXE path
        ttk.Label(frame, text="Default Bot EXE Path:").pack(anchor="w")
        self.exe_var = tk.StringVar(value=self.settings["general"]["default_exe_path"])
        ttk.Entry(frame, textvariable=self.exe_var).pack(fill="x", pady=3)

        # Avatar
        ttk.Label(frame, text="Default Avatar File:").pack(anchor="w")
        self.avatar_var = tk.StringVar(value=self.settings["general"]["default_avatar"])
        ttk.Entry(frame, textvariable=self.avatar_var).pack(fill="x", pady=3)

    def save(self):
        self.settings["general"]["bot_name"] = self.bot_name_var.get()
        self.settings["general"]["model"] = self.model_var.get()
        self.settings["general"]["model_endpoint"] = self.endpoint_var.get()
        self.settings["general"]["auto_launch"] = self.auto_launch_var.get()
        self.settings["general"]["default_exe_path"] = self.exe_var.get()
        self.settings["general"]["default_avatar"] = self.avatar_var.get()
