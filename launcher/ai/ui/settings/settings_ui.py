import tkinter as tk
from tkinter import ttk
from .settings_window import SettingsWindow


class SettingsUI:
    """
    Wrapper for opening the Settings window.
    Integrates:
    - General settings
    - LLM settings
    - Performance settings
    - AI Behavior tab
    - AI Performance tab
    """

    def __init__(self, root, settings, controller_ai, controller_bots):
        self.root = root
        self.settings = settings
        self.controller_ai = controller_ai
        self.controller_bots = controller_bots

        # Window instance (only one allowed)
        self.window = None

    # ---------------------------------------------------------
    # Open Settings Window
    # ---------------------------------------------------------
    def open(self):
        # Prevent multiple windows
        if self.window and tk.Toplevel.winfo_exists(self.window):
            self.window.focus()
            return

        self.window = tk.Toplevel(self.root)
        self.window.title("Settings")
        self.window.geometry("900x600")
        self.window.minsize(850, 550)

        # Windows theme
        self._apply_theme()

        # Create settings window with controllers
        SettingsWindow(
            root=self.window,
            settings=self.settings,
            controller_ai=self.controller_ai,
            controller_bots=self.controller_bots
        )

        # Modal behavior
        self.window.transient(self.root)
        self.window.grab_set()
        self.window.focus()

    # ---------------------------------------------------------
    # Apply Windows theme + fonts
    # ---------------------------------------------------------
    def _apply_theme(self):
        style = ttk.Style()
        try:
            style.theme_use("vista")
        except:
            style.theme_use("default")

        self.root.option_add("*Font", "Segoe UI 10")
