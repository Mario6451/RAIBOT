# launcher/ui/ui_plugins_tab.py

import tkinter as tk
from tkinter import ttk


def build_plugins_tab(ui):
    frame = ui.plugins_tab

    ttk.Label(frame, text="🔌 Plugins", font=("Segoe UI", 14, "bold")).pack(pady=5)

    ui.plugin_list = tk.Listbox(frame, height=18, width=70)
    ui.plugin_list.pack(pady=10)

    btn_frame = ttk.Frame(frame)
    btn_frame.pack(pady=5)

    ui.enable_plugin_btn = ttk.Button(btn_frame, text="✅ Enable")
    ui.enable_plugin_btn.grid(row=0, column=0, padx=10)

    ui.disable_plugin_btn = ttk.Button(btn_frame, text="❌ Disable")
    ui.disable_plugin_btn.grid(row=0, column=1, padx=10)

    def set_plugins(plugins):
        ui.plugin_list.delete(0, "end")
        for p in plugins:
            ui.plugin_list.insert("end", p)

    ui.set_plugins = set_plugins
