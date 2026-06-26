# launcher/ui/ui_window_tab.py

from tkinter import ttk


def build_window_tab(ui):
    frame = ui.window_tab

    ttk.Label(frame, text="🪟 Window Viewer", font=("Segoe UI", 16, "bold")).pack(pady=5)

    ui.window_container = ttk.Frame(frame)
    ui.window_container.pack(fill="both", expand=True, padx=10, pady=10)

    ui.refresh_windows_btn = ttk.Button(frame, text="🔄 Refresh Windows")
    ui.refresh_windows_btn.pack(pady=5)

    def set_window_list(windows):
        for child in ui.window_container.winfo_children():
            child.destroy()

        cols = 3
        row = 0
        col = 0

        for win in windows:
            card = ttk.Frame(ui.window_container, relief="ridge", borderwidth=1)
            card.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")

            title = win.get("title", "")
            pid = win.get("pid", "")
            pname = win.get("process_name", "")
            tag = win.get("tag", "")

            ttk.Label(card, text=f"🪟 {title}", font=("Segoe UI", 10, "bold")).pack(anchor="w", padx=5, pady=2)
            ttk.Label(card, text=f"PID: {pid}  {pname}{tag}", font=("Segoe UI", 9)).pack(anchor="w", padx=5)

            btns = ttk.Frame(card)
            btns.pack(pady=5)

            focus_btn = ttk.Button(btns, text="🎯 Focus")
            focus_btn.pack(side="left", padx=3)

            minimize_btn = ttk.Button(btns, text="➖ Minimize")
            minimize_btn.pack(side="left", padx=3)

            close_btn = ttk.Button(btns, text="❌ Close")
            close_btn.pack(side="left", padx=3)

            focus_btn.config(command=lambda h=win.get("handle"): ui.controller.focus_window(h))
            minimize_btn.config(command=lambda h=win.get("handle"): ui.controller.minimize_window(h))
            close_btn.config(command=lambda h=win.get("handle"): ui.controller.close_window(h))

            col += 1
            if col >= cols:
                col = 0
                row += 1

    ui.set_window_list = set_window_list
