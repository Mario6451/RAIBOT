# ui/settings/performance_tab.py

import tkinter as tk
from tkinter import ttk

class PerformanceTab:
    def __init__(self, parent, settings):
        self.settings = settings
        self.frame = ttk.Frame(parent)
        self.build()

    def build(self):
        frame = ttk.LabelFrame(self.frame, text="Performance Settings")
        frame.pack(fill="x", padx=10, pady=10)

        # Tick rate
        ttk.Label(frame, text="AI Tick Rate (Hz):").pack(anchor="w")
        self.tick_var = tk.IntVar(value=self.settings["performance"]["tick_rate"])
        ttk.Entry(frame, textvariable=self.tick_var).pack(fill="x", pady=3)

        # Capture FPS
        ttk.Label(frame, text="Screen Capture FPS:").pack(anchor="w")
        self.capture_var = tk.IntVar(value=self.settings["performance"]["capture_fps"])
        ttk.Entry(frame, textvariable=self.capture_var).pack(fill="x", pady=3)

        # Pathfinding grid size
        ttk.Label(frame, text="Pathfinding Grid Size:").pack(anchor="w")
        self.grid_var = tk.IntVar(value=self.settings["performance"]["pathfinding_grid_size"])
        ttk.Entry(frame, textvariable=self.grid_var).pack(fill="x", pady=3)

        # Logging toggle
        self.log_var = tk.BooleanVar(value=self.settings["performance"]["logging_enabled"])
        ttk.Checkbutton(
            frame,
            text="Enable Logging",
            variable=self.log_var
        ).pack(anchor="w", pady=3)

    def save(self):
        self.settings["performance"]["tick_rate"] = self.tick_var.get()
        self.settings["performance"]["capture_fps"] = self.capture_var.get()
        self.settings["performance"]["pathfinding_grid_size"] = self.grid_var.get()
        self.settings["performance"]["logging_enabled"] = self.log_var.get()
