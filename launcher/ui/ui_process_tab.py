# launcher/ui/ui_process_tab.py

import tkinter as tk
from tkinter import ttk


def build_process_tab(ui):
    frame = ui.process_tab

    ttk.Label(frame, text="🧩 Process List", font=("Segoe UI", 16, "bold")).pack(pady=5)

    ui.process_list = tk.Listbox(frame, height=28, width=130)
    ui.process_list.pack(pady=10)

    def set_process_list(items):
        ui.process_list.delete(0, "end")
        for item in items:
            ui.process_list.insert("end", item)

    ui.set_process_list = set_process_list
