# ui/ui_main.py

import tkinter as tk
from tkinter import ttk

# UI tabs
from ui.ui_launcher_tab import LauncherTab
from ui.ui_bots_tab import BotsTab
from ui.ui_avatar_converter_tab import AvatarConverterTab

# Controllers
from controller.controller_launcher import LauncherController
from controller.controller_bots import BotsController
from controller.controller_avatar_converter import AvatarConverterController


class MainUI:
    def __init__(self, root, main):
        self.root = root
        self.main = main

        self.tabs = ttk.Notebook(root)
        self.tabs.pack(fill="both", expand=True)

        # Controllers
        self.launcher_controller = LauncherController(main)
        self.bots_controller = BotsController(main)
        self.avatar_converter_controller = AvatarConverterController(main)

        # Tabs
        self.launcher = LauncherTab(self.tabs, self.launcher_controller)
        self.bots = BotsTab(self.tabs, self.bots_controller)
        self.avatar_converter = AvatarConverterTab(self.tabs, self.avatar_converter_controller)

        # Add tabs to UI
        self.tabs.add(self.launcher, text="Launcher")
        self.tabs.add(self.bots, text="Bots")
        self.tabs.add(self.avatar_converter, text="Avatar Converter")

    # ---------------------------------------------------------
    # INITIALIZE VERSION DROPDOWNS
    # ---------------------------------------------------------
    def init_versions(self):
        versions = self.main.settings.settings["launcher"]["versions"].split(",")

        # Launcher tab version dropdown
        self.launcher.version_dropdown["values"] = versions
        self.launcher.version_var.set(self.main.settings.settings["launcher"]["version"])

        # Avatar converter version dropdown
        self.avatar_converter.version_dropdown["values"] = versions
        self.avatar_converter.version_var.set(self.main.settings.settings["launcher"]["version"])

    # ---------------------------------------------------------
    # INITIALIZE BOT LIST
    # ---------------------------------------------------------
    def init_bots(self):
        import os
        bots = []

        if os.path.exists("bots"):
            for name in os.listdir("bots"):
                if os.path.isdir(os.path.join("bots", name)):
                    bots.append(name)

        self.launcher.bot_selector["values"] = bots
        if bots:
            self.launcher.bot_selector.set(bots[0])
