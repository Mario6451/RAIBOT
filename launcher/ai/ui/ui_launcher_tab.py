# ui/ui_launcher_tab.py

import tkinter as tk
from tkinter import ttk

# Live Bot Monitor Window
from launcher.ai.ui.live_bot_window import LiveBotWindow


class LauncherTab(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # ---------------------------------------------------------
        # TITLE
        # ---------------------------------------------------------
        ttk.Label(self, text="Launcher", font=("Segoe UI", 16, "bold")).grid(
            row=0, column=0, columnspan=3, pady=(10, 15)
        )

        # ---------------------------------------------------------
        # BOT SELECTION
        # ---------------------------------------------------------
        ttk.Label(self, text="Bot:", font=("Segoe UI", 10)).grid(row=1, column=0, sticky="w", padx=5)
        self.bot_selector = ttk.Combobox(self, state="readonly")
        self.bot_selector.grid(row=1, column=1, sticky="ew", padx=5)

        # ---------------------------------------------------------
        # CLIENT PATH
        # ---------------------------------------------------------
        ttk.Label(self, text="Client Path:", font=("Segoe UI", 10)).grid(row=2, column=0, sticky="w", padx=5)
        self.client_path_var = tk.StringVar()
        ttk.Entry(self, textvariable=self.client_path_var).grid(row=2, column=1, sticky="ew", padx=5)
        ttk.Button(self, text="Browse", command=self.controller.browse_client_path).grid(row=2, column=2, padx=5)

        # ---------------------------------------------------------
        # VERSION SELECTOR
        # ---------------------------------------------------------
        ttk.Label(self, text="Version:", font=("Segoe UI", 10)).grid(row=3, column=0, sticky="w", padx=5)
        self.version_var = tk.StringVar()
        self.version_dropdown = ttk.Combobox(self, textvariable=self.version_var, state="readonly")
        self.version_dropdown.grid(row=3, column=1, sticky="ew", padx=5)

        # ---------------------------------------------------------
        # CONTROL BUTTONS
        # ---------------------------------------------------------
        ttk.Button(self, text="Start Bot", command=self.controller.start_bot).grid(
            row=4, column=0, pady=10, padx=5
        )
        ttk.Button(self, text="Stop Bot", command=self.controller.stop_bot).grid(
            row=4, column=1, pady=10, padx=5
        )
        ttk.Button(self, text="Restart Bot", command=self.controller.restart_bot).grid(
            row=4, column=2, pady=10, padx=5
        )

        # ---------------------------------------------------------
        # LIVE BOT MONITOR BUTTON
        # ---------------------------------------------------------
        ttk.Button(
            self,
            text="Open Live Bot Monitor",
            command=self.open_live_bot_monitor
        ).grid(row=5, column=0, columnspan=3, pady=(5, 10))

        # ---------------------------------------------------------
        # LOG BOX
        # ---------------------------------------------------------
        ttk.Label(self, text="Launcher Log:", font=("Segoe UI", 10, "bold")).grid(
            row=6, column=0, columnspan=3, sticky="w", padx=5
        )

        self.log_box = tk.Text(self, height=12)
        self.log_box.grid(row=7, column=0, columnspan=3, sticky="nsew", padx=5, pady=5)

        # ---------------------------------------------------------
        # GRID CONFIG
        # ---------------------------------------------------------
        self.columnconfigure(1, weight=1)
        self.rowconfigure(7, weight=1)

    # ---------------------------------------------------------
    # LOGGING
    # ---------------------------------------------------------
    def log_launcher(self, text):
        self.log_box.insert("end", text + "\n")
        self.log_box.see("end")

    # ---------------------------------------------------------
    # OPEN LIVE BOT MONITOR WINDOW
    # ---------------------------------------------------------
    def open_live_bot_monitor(self):
        LiveBotWindow(
            parent=self,
            controller_ai=self.controller.main.controller_ai,
            on_select=self.on_bot_selected
        )

    # ---------------------------------------------------------
    # OPTIONAL: SELECT BOT IN EDIT BOT TAB
    # ---------------------------------------------------------
    def on_bot_selected(self, bot):
        # If you want clicking a bot to jump to Edit Bot Tab:
        try:
            ui = self.controller.main.ui  # main UI reference
            ui.edit_bot_panel.select_bot(bot)
            ui.tabs.select(ui.edit_bot_tab)
        except:
            pass
