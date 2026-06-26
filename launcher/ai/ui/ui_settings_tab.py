# launcher/ui/ui_settings_tab.py

import tkinter as tk
from tkinter import ttk


def build_settings_tab(ui):
    frame = ui.settings_tab

    ttk.Label(frame, text="⚙️ Settings", font=("Segoe UI", 14, "bold")).pack(pady=5)

    ui.settings_tree = ttk.Treeview(frame, columns=("key", "value"), show="headings")
    ui.settings_tree.heading("key", text="Key")
    ui.settings_tree.heading("value", text="Value")
    ui.settings_tree.pack(fill="both", expand=True, pady=10)

    edit_frame = ttk.Frame(frame)
    edit_frame.pack(pady=5)

    ttk.Label(edit_frame, text="Key:").grid(row=0, column=0, padx=5)
    ui.settings_key_var = tk.StringVar()
    ttk.Entry(edit_frame, textvariable=ui.settings_key_var, width=30).grid(row=0, column=1, padx=5)

    ttk.Label(edit_frame, text="Value:").grid(row=0, column=2, padx=5)
    ui.settings_value_var = tk.StringVar()
    ttk.Entry(edit_frame, textvariable=ui.settings_value_var, width=30).grid(row=0, column=3, padx=5)

    ui.settings_save_btn = ttk.Button(edit_frame, text="💾 Save Setting")
    ui.settings_save_btn.grid(row=0, column=4, padx=5)

    def set_settings(settings_dict):
        for row in ui.settings_tree.get_children():
            ui.settings_tree.delete(row)
        for k, v in settings_dict.items():
            ui.settings_tree.insert("", "end", values=(k, v))

    ui.set_settings = set_settings
