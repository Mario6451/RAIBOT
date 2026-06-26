# launcher/ui/ui_personality_tab.py

import tkinter as tk
from tkinter import ttk


def build_personality_tab(ui):
    frame = ui.personality_tab

    ttk.Label(frame, text="🧠 Personality", font=("Segoe UI", 14, "bold")).pack(pady=5)

    ui.persona_text = tk.Text(frame, height=20, width=100)
    ui.persona_text.pack(pady=10)

    btn_frame = ttk.Frame(frame)
    btn_frame.pack(pady=5)

    ui.save_persona_btn = ttk.Button(btn_frame, text="💾 Save")
    ui.save_persona_btn.grid(row=0, column=0, padx=5)

    ui.load_persona_btn = ttk.Button(btn_frame, text="📂 Load")
    ui.load_persona_btn.grid(row=0, column=1, padx=5)

    ui.reset_persona_btn = ttk.Button(btn_frame, text="♻ Reset")
    ui.reset_persona_btn.grid(row=0, column=2, padx=5)

    ui.apply_persona_btn = ttk.Button(btn_frame, text="✅ Apply")
    ui.apply_persona_btn.grid(row=0, column=3, padx=5)

    ui.export_persona_btn = ttk.Button(btn_frame, text="📤 Export")
    ui.export_persona_btn.grid(row=0, column=4, padx=5)

    ui.import_persona_btn = ttk.Button(btn_frame, text="📥 Import")
    ui.import_persona_btn.grid(row=0, column=5, padx=5)

    preset_frame = ttk.Frame(frame)
    preset_frame.pack(pady=5)

    ui.preset_roblox_btn = ttk.Button(preset_frame, text="🎮 Roblox‑like")
    ui.preset_roblox_btn.grid(row=0, column=0, padx=5)

    ui.preset_ai_btn = ttk.Button(preset_frame, text="🤖 AI‑like")
    ui.preset_ai_btn.grid(row=0, column=1, padx=5)

    ui.preset_hybrid_btn = ttk.Button(preset_frame, text="⚡ Hybrid")
    ui.preset_hybrid_btn.grid(row=0, column=2, padx=5)
