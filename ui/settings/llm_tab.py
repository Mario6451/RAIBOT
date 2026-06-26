# ui/settings/llm_tab.py

import tkinter as tk
from tkinter import ttk

class LLMTab:
    def __init__(self, parent, settings):
        self.settings = settings
        self.frame = ttk.Frame(parent)
        self.build()

    def build(self):
        frame = ttk.LabelFrame(self.frame, text="LLM Settings")
        frame.pack(fill="x", padx=10, pady=10)

        # Temperature
        ttk.Label(frame, text="Temperature:").pack(anchor="w")
        self.temp_var = tk.DoubleVar(value=self.settings["llm"]["temperature"])
        ttk.Entry(frame, textvariable=self.temp_var).pack(fill="x", pady=3)

        # Max tokens
        ttk.Label(frame, text="Max Tokens:").pack(anchor="w")
        self.tokens_var = tk.IntVar(value=self.settings["llm"]["max_tokens"])
        ttk.Entry(frame, textvariable=self.tokens_var).pack(fill="x", pady=3)

        # System prompt
        ttk.Label(frame, text="System Prompt:").pack(anchor="w")
        self.prompt_text = tk.Text(frame, height=14, wrap="word")
        self.prompt_text.insert("1.0", self.settings["llm"]["system_prompt"])
        self.prompt_text.pack(fill="x", pady=3)

    def save(self):
        self.settings["llm"]["temperature"] = self.temp_var.get()
        self.settings["llm"]["max_tokens"] = self.tokens_var.get()
        self.settings["llm"]["system_prompt"] = self.prompt_text.get("1.0", "end").strip()
