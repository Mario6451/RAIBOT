# ai/ui/personality_editor_tab.py

import tkinter as tk
from tkinter import ttk

class PersonalityEditorTab(ttk.Frame):
    def __init__(self, parent, editor):
        super().__init__(parent)
        self.editor = editor

        ttk.Label(self, text="Personality Editor", font=("Segoe UI", 14, "bold")).pack(pady=10)

        # Slot selector
        ttk.Label(self, text="Custom Personality Slot (64–127):").pack()
        self.slot_var = tk.StringVar()
        self.slot_dropdown = ttk.Combobox(self, textvariable=self.slot_var, state="readonly")
        self.slot_dropdown.pack(pady=5)

        # Name field
        ttk.Label(self, text="Personality Name:").pack()
        self.name_var = tk.StringVar()
        ttk.Entry(self, textvariable=self.name_var).pack(pady=5)

        # Config editor (simple key/value)
        ttk.Label(self, text="Config (key=value per line):").pack()
        self.config_text = tk.Text(self, height=10, width=40)
        self.config_text.pack(pady=5)

        # Save button
        ttk.Button(self, text="Save Personality", command=self.save_profile).pack(pady=10)

        self.refresh()

    def refresh(self):
        slots = self.editor.list_custom_slots()
        self.slot_dropdown["values"] = [str(pid) for pid, _ in slots]

    def save_profile(self):
        pid = int(self.slot_var.get())
        name = self.name_var.get()

        # Parse config text
        config = {}
        for line in self.config_text.get("1.0", tk.END).splitlines():
            if "=" in line:
                key, value = line.split("=", 1)
                key = key.strip()
                value = value.strip()

                # Try to convert numbers
                try:
                    value = float(value)
                except:
                    pass

                config[key] = value

        self.editor.save_custom_profile(pid, name, config)
