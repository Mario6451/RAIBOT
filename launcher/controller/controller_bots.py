# launcher/controller/controller_bots.py

import subprocess
import threading
import tkinter as tk
from tkinter import filedialog
import os
import psutil
from bot.bot_runtime import run_bot
import json


class BotController:
    def __init__(self, main):
        self.main = main
        self.ui = main.ui

    # ---------------------------------------------------------
    # START BOT
    # ---------------------------------------------------------
    def start_bot(self):
        bot_name = self.ui.launcher.bot_selector.get()
        cfg = self.main.settings.settings

        # Load behavior-only profile.json
        profile_path = f"bots/{bot_name}/profile.json"
        if os.path.exists(profile_path):
            with open(profile_path, "r", encoding="utf8") as f:
                behavior = json.load(f)
        else:
            behavior = {"Behavior": {}}

        config = {
            "bot_name": bot_name,
            "server_ip": cfg["server"]["ip"],
            "server_port": cfg["server"]["port"],
            "settings": cfg,
            "behavior": behavior["Behavior"]
        }

        self.ui.launcher.log_launcher(f"Starting bot: {bot_name}")

        threading.Thread(target=lambda: run_bot(config), daemon=True).start()

    # ---------------------------------------------------------
    # STOP BOT
    # ---------------------------------------------------------
    def stop_bot(self):
        self.ui.launcher.log_launcher("Stopping bot...")

        for p in psutil.process_iter(["cmdline"]):
            cmd = p.info["cmdline"] or []
            if "RobloxPlayerBeta.exe" in " ".join(cmd):
                try:
                    p.terminate()
                except:
                    pass

        self.ui.launcher.log_launcher("Bot stopped.")

    # ---------------------------------------------------------
    # RESTART BOT
    # ---------------------------------------------------------
    def restart_bot(self):
        self.stop_bot()
        self.start_bot()

    # ---------------------------------------------------------
    # FILE BROWSING
    # ---------------------------------------------------------
    def browse_client_path(self):
        path = filedialog.askopenfilename(title="Select Roblox Client")
        if path:
            self.ui.launcher.client_path_var.set(path)
            self.main.settings.settings["launcher"]["client_path"] = path
            self.main.save_settings()

    def browse_joinscript(self):
        path = filedialog.askopenfilename(title="Select JoinScript")
        if path:
            self.ui.launcher.joinscript_var.set(path)
            self.main.settings.settings["launcher"]["joinscript_path"] = path
            self.main.save_settings()
