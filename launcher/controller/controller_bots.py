import os
import json
import threading
import psutil
from tkinter import filedialog

from launcher.features.bot_autocreate import create_bot_folder
from launcher.bot.bot_loader import load_avatar
from launcher.bot.bot_launcher import launch_bot


class BotsController:
    def __init__(self, main):
        self.main = main
        self.ui = main.ui

    def create_bot(self):
        name = self.ui.bots.new_bot_name.get().strip()
        if not name:
            self.ui.bots.show_status("Enter a bot name.")
            return

        create_bot_folder(name)
        self.ui.bots.show_status(f"Bot '{name}' created.")
        self.main.reload_bot_list()

    def start_bot(self):
        bot_name = self.ui.launcher.bot_selector.get()
        settings = self.main.settings.settings

        avatar_path = f"bots/{bot_name}/avatar.ini"
        if not os.path.exists(avatar_path):
            self.ui.launcher.log_launcher("Missing avatar.ini for bot.")
            return

        avatar = load_avatar(avatar_path)

        extra = {
            "placeid": settings["launcher"]["place_id"],
            "ip": settings["server"]["ip"],
            "port": settings["server"]["port"],
            "user": bot_name,
            "id": "1",
            "mship": "None"
        }

        version = settings["launcher"]["version"]
        url = launch_bot(settings, avatar, version, extra)

        self.ui.launcher.log_launcher(f"Launching bot {bot_name}")
        self.ui.launcher.log_launcher(f"Join URL: {url}")

        threading.Thread(target=lambda: os.system(
            f'"{settings["launcher"]["client_path"]}" -j "{url}"'
        ), daemon=True).start()

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

    def restart_bot(self):
        self.stop_bot()
        self.start_bot()

    def browse_client_path(self):
        path = filedialog.askopenfilename(title="Select Roblox Client")
        if path:
            self.ui.launcher.client_path_var.set(path)
            self.main.settings.settings["launcher"]["client_path"] = path
            self.main.save_settings()
