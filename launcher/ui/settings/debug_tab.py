# ui/settings/debug_tab.py

import tkinter as tk
from tkinter import ttk

class DebugTab:
    def __init__(self, parent):
        self.frame = ttk.Frame(parent)
        self.build()

    def build(self):
        frame = ttk.LabelFrame(self.frame, text="AI Debug Console")
        frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Scrollable text widget
        text_frame = ttk.Frame(frame)
        text_frame.pack(fill="both", expand=True)

        self.debug_text = tk.Text(
            text_frame,
            height=20,
            wrap="word",
            font=("Segoe UI", 10)
        )
        self.debug_text.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(
            text_frame,
            orient="vertical",
            command=self.debug_text.yview
        )
        scrollbar.pack(side="right", fill="y")

        self.debug_text.configure(yscrollcommand=scrollbar.set)

        # Clear button
        ttk.Button(
            frame,
            text="Clear Log",
            command=lambda: self.debug_text.delete("1.0", "end")
        ).pack(pady=5)

    # Called by AIBrain or any module
    def log(self, text):
        self.debug_text.insert("end", text + "\n")
        self.debug_text.see("end")
