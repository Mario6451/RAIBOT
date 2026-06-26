# ui/settings/training_tab.py

import tkinter as tk
from tkinter import ttk

class TrainingTab:
    def __init__(self, parent, settings):
        self.settings = settings
        self.frame = ttk.Frame(parent)
        self.build()

    def build(self):
        frame = ttk.LabelFrame(self.frame, text="AI Training Settings")
        frame.pack(fill="x", padx=10, pady=10)

        # Self-learning
        self.self_var = tk.BooleanVar(value=self.settings["training"]["self_learning"])
        ttk.Checkbutton(
            frame,
            text="Enable Self-Learning (AI learns from its own gameplay)",
            variable=self.self_var
        ).pack(anchor="w", pady=3)

        # Imitation learning
        self.imitation_var = tk.BooleanVar(value=self.settings["training"]["imitation_learning"])
        ttk.Checkbutton(
            frame,
            text="Enable Imitation Learning (AI learns from watching you play)",
            variable=self.imitation_var
        ).pack(anchor="w", pady=3)

        # Instruction learning
        self.instruction_var = tk.BooleanVar(value=self.settings["training"]["instruction_learning"])
        ttk.Checkbutton(
            frame,
            text="Enable Instruction Learning (AI learns from what you tell it)",
            variable=self.instruction_var
        ).pack(anchor="w", pady=3)

    def save(self):
        self.settings["training"]["self_learning"] = self.self_var.get()
        self.settings["training"]["imitation_learning"] = self.imitation_var.get()
        self.settings["training"]["instruction_learning"] = self.instruction_var.get()
