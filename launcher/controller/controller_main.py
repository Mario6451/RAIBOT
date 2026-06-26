# launcher/controller/controller_main.py

from .controller_settings import SettingsController
from .controller_webui import WebUIController
from .controller_bots import BotController
from .controller_windows import WindowController
from .controller_plugins import PluginController
from .controller_personality import PersonalityController
from .controller_processes import ProcessController


class LauncherController:
    def __init__(self, ui):
        self.ui = ui
        self.ui.attach_controller(self)

        # Sub‑controllers
        self.settings = SettingsController(self)
        self.webui = WebUIController(self)
        self.bots = BotController(self)
        self.windows = WindowController(self)
        self.plugins = PluginController(self)
        self.personality = PersonalityController(self)
        self.processes = ProcessController(self)

        # Load settings
        self.settings.load()

        # Start Web‑UI server
        self.webui.start_server()

        # Load plugins, processes, windows, persona
        self.plugins.load_plugins()
        self.processes.load_processes()
        self.windows.refresh_windows()
        self.personality.load_persona()

        # Update UI preview
        self.bots.update_preview()

    # ---------------------------------------------------------
    # UI → Controller routing
    # ---------------------------------------------------------

    # Bots
    def start_bot(self): self.bots.start_bot()
    def stop_bot(self): self.bots.stop_bot()
    def restart_bot(self): self.bots.restart_bot()
    def refresh_status(self): self.bots.refresh_status()
    def on_bot_selected(self, event): self.bots.on_bot_selected(event)
    def add_bot(self): self.bots.add_bot()
    def edit_current_bot(self): self.bots.edit_current_bot()

    # Client paths
    def browse_client_path(self): self.bots.browse_client_path()
    def browse_joinscript(self): self.bots.browse_joinscript()

    # Windows
    def refresh_windows(self): self.windows.refresh_windows()
    def focus_window(self, h): self.windows.focus_window(h)
    def minimize_window(self, h): self.windows.minimize_window(h)
    def close_window(self, h): self.windows.close_window(h)

    # Plugins
    def enable_selected_plugin(self): self.plugins.enable_selected_plugin()
    def disable_selected_plugin(self): self.plugins.disable_selected_plugin()

    # Settings
    def save_setting(self): self.settings.save_setting()
    def on_setting_selected(self, event): self.settings.on_setting_selected(event)

    # Personality
    def save_persona(self): self.personality.save_persona()
    def load_persona(self): self.personality.load_persona()
    def reset_persona(self): self.personality.reset_persona()
    def apply_persona(self): self.personality.apply_persona()
    def export_persona(self): self.personality.export_persona()
    def import_persona(self): self.personality.import_persona()
    def apply_preset(self, preset): self.personality.apply_preset(preset)

    # Web‑UI
    def open_dashboard(self): self.webui.open_dashboard()
    def open_logs(self): self.webui.open_logs()
