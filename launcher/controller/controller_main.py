# launcher/controller/controller_main.py

import json
import os
from launcher.controller.controller_bots import BotController
from launcher.controller.controller_webui import WebUIController


class MainController:
    def __init__(self, ui, settings):
        self.ui = ui
        self.settings = settings

        self.bots = BotController(self)
        self.webui = WebUIController(self)

        self._load_initial_ui()

    # ---------------------------------------------------------
    # INITIAL UI LOAD
    # ---------------------------------------------------------
    def _load_initial_ui(self):
        cfg = self.settings.settings

        # Load bot list
        bot_names = os.listdir("bots")
        self.ui.launcher.bot_selector["values"] = bot_names
        if bot_names:
            self.ui.launcher.bot_selector.set(bot_names[0])

        # Load client path
        self.ui.launcher.client_path_var.set(cfg["launcher"]["client_path"])
        self.ui.launcher.joinscript_var.set(cfg["launcher"]["joinscript_path"])

        # Load server IP/port
        self.ui.launcher.server_ip_var.set(cfg["server"]["ip"])
        self.ui.launcher.server_port_var.set(cfg["server"]["port"])

    # ---------------------------------------------------------
    # SETTINGS SAVE
    # ---------------------------------------------------------
    def save_settings(self):
        with open("settings/settings.json", "w", encoding="utf8") as f:
            json.dump(self.settings.settings, f, indent=4)
        self.ui.launcher.log_global("Settings saved.")

    # ---------------------------------------------------------
    # UI CALLBACKS
    # ---------------------------------------------------------
    def on_bot_selected(self, event=None):
        bot = self.ui.launcher.bot_selector.get()
        self.ui.launcher.log_launcher(f"Selected bot: {bot}")

    def start_bot(self):
        self.bots.start_bot()

    def stop_bot(self):
        self.bots.stop_bot()

    def restart_bot(self):
        self.bots.restart_bot()

    def open_dashboard(self):
        self.webui.open_dashboard()

    def restart_server(self):
        self.webui.restart_server()

    def open_logs(self):
        self.webui.open_logs()

    def browse_client_path(self):
        self.bots.browse_client_path()

    def browse_joinscript(self):
        self.bots.browse_joinscript()
