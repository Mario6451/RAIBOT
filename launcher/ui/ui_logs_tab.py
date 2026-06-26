# launcher/ui/ui_logs_tab.py

import tkinter as tk
from tkinter import ttk


def build_logs_tab(ui):
    frame = ui.logs_tab

    ttk.Label(frame, text="📜 Logs", font=("Segoe UI", 14, "bold")).pack(pady=5)

    ui.log_box = tk.Text(frame, height=28, width=130, state="disabled")
    ui.log_box.pack(pady=10)

    def log_global(text):
        ui.log_box.config(state="normal")
        ui.log_box.insert("end", text + "\n")
        ui.log_box.see("end")
        ui.log_box.config(state="disabled")

    ui.log_global = log_global
