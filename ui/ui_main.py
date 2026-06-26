import os
import json
import tkinter as tk
from tkinter import ttk
import webbrowser

from bot_runtime import run_bot

from ui_personality_tab import build_personality_tab
from ui_logs_tab import build_logs_tab
from ui_settings_tab import build_settings_tab
from ui_plugins_tab import build_plugins_tab
from ui_window_tab import build_window_tab
from ui_process_tab import build_process_tab
from ui_map_tab import build_map_tab
from ui_launcher_tab import build_launcher_tab


class MainUI:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Roblox AI Player")

        self.launcher_settings = self._load_launcher_settings()

        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill="both", expand=True)

        self.launcher_tab = ttk.Frame(self.notebook)
        self.personality_tab = ttk.Frame(self.notebook)
        self.logs_tab = ttk.Frame(self.notebook)
        self.settings_tab = ttk.Frame(self.notebook)
        self.plugins_tab = ttk.Frame(self.notebook)
        self.window_tab = ttk.Frame(self.notebook)
        self.process_tab = ttk.Frame(self.notebook)
        self.map_tab = ttk.Frame(self.notebook)

        self.notebook.add(self.launcher_tab, text="Launcher")
        self.notebook.add(self.personality_tab, text="Personality")
        self.notebook.add(self.logs_tab, text="Logs")
        self.notebook.add(self.settings_tab, text="Settings")
        self.notebook.add(self.plugins_tab, text="Plugins")
        self.notebook.add(self.window_tab, text="Window")
        self.notebook.add(self.process_tab, text="Process")
        self.notebook.add(self.map_tab, text="Map")

        build_launcher_tab(self)
        build_personality_tab(self)
        build_logs_tab(self)
        build_settings_tab(self)
        build_plugins_tab(self)
        build_window_tab(self)
        build_process_tab(self)
        build_map_tab(self)

    def _load_launcher_settings(self):
        os.makedirs("settings", exist_ok=True)
        path = os.path.join("settings", "launcher.json")
        if not os.path.exists(path):
            return {
                "client_path": "",
                "joinscript_url": "https://www.rbolock.tk/game/join2017.php",
                "place_id": "0",
                "web_ui_port": 5000
            }
        with open(path, "r", encoding="utf8") as f:
            return json.load(f)

    def save_setting(self, key, value):
        self.launcher_settings[key] = value
        os.makedirs("settings", exist_ok=True)
        with open("settings/launcher.json", "w", encoding="utf8") as f:
            json.dump(self.launcher_settings, f, indent=4)

    def load_setting(self, key, default=""):
        return self.launcher_settings.get(key, default)

    def start_bot(self):
        bot_name = self.bot_selector.get()

        config = {
            "bot_name": bot_name,
            "server_ip": self.server_ip_var.get(),
            "server_port": int(self.server_port_var.get()),
            "settings": {
                "launcher": self.launcher_settings,
                "performance": {"tick_rate": 30},
                "movement": {"use_mouse_look": True},
                "training": {
                    "self_learning": True,
                    "imitation_learning": True,
                    "instruction_learning": True
                }
            }
        }

        self.log_launcher(f"Starting bot: {bot_name}")
        self.update_status("Starting...")
        run_bot(config)

    def stop_bot(self):
        self.log_launcher("Stop requested (not implemented).")
        self.update_status("Stop requested")

    def restart_bot(self):
        self.log_launcher("Restart requested (not implemented).")
        self.update_status("Restart requested")

    def refresh_bots(self):
        self.log_launcher("Refresh requested (not implemented).")

    def open_dashboard(self):
        port = int(self.launcher_settings.get("web_ui_port", 5000))
        url = f"http://localhost:{port}"
        self.log_launcher(f"Opening Web‑UI: {url}")
        webbrowser.open(url)

    def open_logs_folder(self):
        logs_path = os.path.join("logs")
        os.makedirs(logs_path, exist_ok=True)
        self.log_launcher(f"Opening logs folder: {logs_path}")
        try:
            os.startfile(logs_path)
        except Exception:
            webbrowser.open(logs_path)


def main():
    root = tk.Tk()
    ui = MainUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
