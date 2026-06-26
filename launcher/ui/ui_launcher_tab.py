import tkinter as tk
from tkinter import ttk

class LauncherTab(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        ttk.Label(self, text="Bot:").grid(row=0, column=0, sticky="w")
        self.bot_selector = ttk.Combobox(self, state="readonly")
        self.bot_selector.grid(row=0, column=1, sticky="ew")

        ttk.Label(self, text="Client Path:").grid(row=1, column=0, sticky="w")
        self.client_path_var = tk.StringVar()
        ttk.Entry(self, textvariable=self.client_path_var).grid(row=1, column=1, sticky="ew")
        ttk.Button(self, text="Browse", command=self.controller.browse_client_path).grid(row=1, column=2)

        ttk.Label(self, text="Version:").grid(row=2, column=0, sticky="w")
        self.version_var = tk.StringVar()
        self.version_dropdown = ttk.Combobox(self, textvariable=self.version_var, state="readonly")
        self.version_dropdown.grid(row=2, column=1, sticky="ew")

        ttk.Button(self, text="Start Bot", command=self.controller.start_bot).grid(row=3, column=0, pady=5)
        ttk.Button(self, text="Stop Bot", command=self.controller.stop_bot).grid(row=3, column=1, pady=5)
        ttk.Button(self, text="Restart Bot", command=self.controller.restart_bot).grid(row=3, column=2, pady=5)

        self.log_box = tk.Text(self, height=10)
        self.log_box.grid(row=4, column=0, columnspan=3, sticky="nsew")

        self.columnconfigure(1, weight=1)
        self.rowconfigure(4, weight=1)

    def log_launcher(self, text):
        self.log_box.insert("end", text + "\n")
        self.log_box.see("end")
