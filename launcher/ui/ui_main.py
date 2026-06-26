# launcher/ui/ui_main.py

import tkinter as tk
from tkinter import ttk

from .ui_launcher_tab import build_launcher_tab
from .ui_map_tab import build_map_tab
from .ui_process_tab import build_process_tab
from .ui_window_tab import build_window_tab
from .ui_plugins_tab import build_plugins_tab
from .ui_settings_tab import build_settings_tab
from .ui_logs_tab import build_logs_tab
from .ui_personality_tab import build_personality_tab


class LauncherUI:
    def __init__(self):
        self.controller = None

        self.root = tk.Tk()
        self.root.title("Roblox AI Player Control Center")
        self.root.geometry("1200x750")
        self.root.resizable(False, False)

        self._build_notebook()

    def _build_notebook(self):
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True)

        self.launcher_tab = ttk.Frame(self.notebook)
        self.map_tab = ttk.Frame(self.notebook)
        self.process_tab = ttk.Frame(self.notebook)
        self.window_tab = ttk.Frame(self.notebook)
        self.plugins_tab = ttk.Frame(self.notebook)
        self.settings_tab = ttk.Frame(self.notebook)
        self.logs_tab = ttk.Frame(self.notebook)
        self.personality_tab = ttk.Frame(self.notebook)

        self.notebook.add(self.launcher_tab, text="🚀 Launcher")
        self.notebook.add(self.map_tab, text="🗺 Map / Viewer")
        self.notebook.add(self.process_tab, text="🧩 Processes")
        self.notebook.add(self.window_tab, text="🪟 Windows")
        self.notebook.add(self.plugins_tab, text="🔌 Plugins")
        self.notebook.add(self.settings_tab, text="⚙️ Settings")
        self.notebook.add(self.logs_tab, text="📜 Logs")
        self.notebook.add(self.personality_tab, text="🧠 Personality")

        build_launcher_tab(self)
        build_map_tab(self)
        build_process_tab(self)
        build_window_tab(self)
        build_plugins_tab(self)
        build_settings_tab(self)
        build_logs_tab(self)
        build_personality_tab(self)

    def attach_controller(self, controller):
        self.controller = controller

        # launcher
        self.start_btn.config(command=self.controller.start_bot)
        self.stop_btn.config(command=self.controller.stop_bot)
        self.restart_btn.config(command=self.controller.restart_bot)
        self.refresh_btn.config(command=self.controller.refresh_status)
        self.open_dashboard_btn.config(command=self.controller.open_dashboard)
        self.open_logs_btn.config(command=self.controller.open_logs)

        # client path
        self.client_browse_btn.config(command=self.controller.browse_client_path)

        # joinscript
        self.joinscript_browse_btn.config(command=self.controller.browse_joinscript)

        # bots
        self.add_bot_btn.config(command=self.controller.add_bot)
        self.edit_bot_btn.config(command=self.controller.edit_current_bot)
        self.bot_selector.bind("<<ComboboxSelected>>", self.controller.on_bot_selected)

        # plugins
        self.enable_plugin_btn.config(command=self.controller.enable_selected_plugin)
        self.disable_plugin_btn.config(command=self.controller.disable_selected_plugin)

        # windows
        self.refresh_windows_btn.config(command=self.controller.refresh_windows)

        # settings
        self.settings_save_btn.config(command=self.controller.save_setting)
        self.settings_tree.bind("<<TreeviewSelect>>", self.controller.on_setting_selected)

        # personality
        self.save_persona_btn.config(command=self.controller.save_persona)
        self.load_persona_btn.config(command=self.controller.load_persona)
        self.reset_persona_btn.config(command=self.controller.reset_persona)
        self.apply_persona_btn.config(command=self.controller.apply_persona)
        self.export_persona_btn.config(command=self.controller.export_persona)
        self.import_persona_btn.config(command=self.controller.import_persona)
        self.preset_roblox_btn.config(command=lambda: self.controller.apply_preset("roblox"))
        self.preset_ai_btn.config(command=lambda: self.controller.apply_preset("ai"))
        self.preset_hybrid_btn.config(command=lambda: self.controller.apply_preset("hybrid"))
def load_setting(self, key, default=""):
    return self.launcher_settings.get(key, default)

def save_setting(self, key, value):
    self.launcher_settings[key] = value
    with open("settings/launcher.json", "w", encoding="utf8") as f:
        json.dump(self.launcher_settings, f, indent=4)
