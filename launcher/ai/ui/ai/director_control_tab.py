# ai/ui/director_control_tab.py

import tkinter as tk
from tkinter import ttk

class DirectorControlTab(ttk.Frame):
    def __init__(self, parent, panel):
        super().__init__(parent)
        self.panel = panel

        ttk.Label(self, text="Director AI Control", font=("Segoe UI", 14, "bold")).pack(pady=10)

        # Enable/Disable
        self.enabled_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(self, text="Enable Director AI", variable=self.enabled_var,
                        command=self.toggle_enabled).pack(pady=5)

        # Mode selector
        ttk.Label(self, text="Director Mode:").pack()
        self.mode_var = tk.StringVar()
        self.mode_dropdown = ttk.Combobox(self, textvariable=self.mode_var, state="readonly",
                                          values=["dynamic", "calm", "intense", "custom"])
        self.mode_dropdown.pack(pady=5)
        self.mode_dropdown.bind("<<ComboboxSelected>>", self.change_mode)

        # Difficulty slider
        ttk.Label(self, text="Difficulty (0.5–2.0):").pack()
        self.difficulty_var = tk.DoubleVar(value=1.0)
        ttk.Scale(self, from_=0.5, to=2.0, orient="horizontal",
                  variable=self.difficulty_var, command=self.change_difficulty).pack(fill="x", padx=20)

        # Aggression slider
        ttk.Label(self, text="Aggression (0.5–2.0):").pack()
        self.aggression_var = tk.DoubleVar(value=1.0)
        ttk.Scale(self, from_=0.5, to=2.0, orient="horizontal",
                  variable=self.aggression_var, command=self.change_aggression).pack(fill="x", padx=20)

        # Manual tension override
        ttk.Label(self, text="Manual Tension Override (0–10):").pack()
        self.tension_var = tk.DoubleVar(value=5.0)
        ttk.Scale(self, from_=0, to=10, orient="horizontal",
                  variable=self.tension_var, command=self.override_tension).pack(fill="x", padx=20)

        ttk.Button(self, text="Clear Manual Override", command=self.clear_override).pack(pady=10)

        # Force personality reassignment
        ttk.Button(self, text="Reassign All Personalities",
                   command=self.panel.reassign_all_personalities).pack(pady=10)

    # ---------------------------------------------------------
    # CALLBACKS
    # ---------------------------------------------------------
    def toggle_enabled(self):
        self.panel.set_enabled(self.enabled_var.get())

    def change_mode(self, event=None):
        self.panel.set_mode(self.mode_var.get())

    def change_difficulty(self, event=None):
        self.panel.set_difficulty(self.difficulty_var.get())

    def change_aggression(self, event=None):
        self.panel.set_aggression(self.aggression_var.get())

    def override_tension(self, event=None):
        self.panel.set_manual_tension(self.tension_var.get())

    def clear_override(self):
        self.panel.clear_manual_override()
