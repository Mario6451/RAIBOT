# ui/ui_main.py

import tkinter as tk
from tkinter import ttk

# Existing UI tabs
from ui.ui_launcher_tab import LauncherTab
from ui.ui_bots_tab import BotsTab
from ui.ui_avatar_converter_tab import AvatarConverterTab

# New AI tabs
from ui.map.ai_map_tab import AIMapTab
from ui.ai.ai_command_tab import AICommandTab
from ui.ai.bot_inspector_tab import BotInspectorTab
from ui.ai.ai_logs_tab import AILogsTab
from ui.ai.path_debug_tab import PathDebugTab
from ui.ai.bot_manager_tab import BotManagerTab
from ui.ai.ai_profiler_tab import AIProfilerTab

# Controllers
from controller.controller_launcher import LauncherController
from controller.controller_bots import BotsController
from controller.controller_avatar_converter import AvatarConverterController


class MainUI:
    def __init__(self, root, main):
        self.root = root
        self.main = main

        # Notebook container
        self.tabs = ttk.Notebook(root)
        self.tabs.pack(fill="both", expand=True)

        # Controllers
        self.launcher_controller = LauncherController(main)
        self.bots_controller = BotsController(main)
        self.avatar_converter_controller = AvatarConverterController(main)

        # NEW: AI controllers from main
        self.controller_ai = main.controller_ai
        self.controller_bots = main.controller_bots

        # ---------------------------------------------------------
        # EXISTING TABS
        # ---------------------------------------------------------
        self.launcher = LauncherTab(self.tabs, self.launcher_controller)
        self.bots = BotsTab(self.tabs, self.bots_controller)
        self.avatar_converter = AvatarConverterTab(self.tabs, self.avatar_converter_controller)

        self.tabs.add(self.launcher, text="Launcher")
        self.tabs.add(self.bots, text="Bots")
        self.tabs.add(self.avatar_converter, text="Avatar Converter")

        # ---------------------------------------------------------
        # NEW AI TABS
        # ---------------------------------------------------------

        # AI Map
        self.ai_map_tab = AIMapTab(self.tabs, self.controller_ai)
        self.tabs.add(self.ai_map_tab, text="AI Map")

        # AI Command Center
        self.ai_command_tab = AICommandTab(self.tabs, self.controller_ai, self.controller_bots)
        self.tabs.add(self.ai_command_tab, text="AI Command")

        # Bot Inspector
        self.bot_inspector_tab = BotInspectorTab(self.tabs, self.controller_ai)
        self.tabs.add(self.bot_inspector_tab, text="Bot Inspector")

        # AI Logs
        self.ai_logs_tab = AILogsTab(self.tabs, self.controller_ai)
        self.tabs.add(self.ai_logs_tab, text="AI Logs")

        # Pathfinding Debugger
        self.path_debug_tab = PathDebugTab(self.tabs, self.controller_ai)
        self.tabs.add(self.path_debug_tab, text="Path Debugger")

        # Bot Manager
        self.bot_manager_tab = BotManagerTab(self.tabs, self.controller_ai, self.controller_bots)
        self.tabs.add(self.bot_manager_tab, text="Bot Manager")

        # AI Profiler
        self.ai_profiler_tab = AIProfilerTab(self.tabs, self.controller_ai)
        self.tabs.add(self.ai_profiler_tab, text="AI Profiler")

    # ---------------------------------------------------------
    # INITIALIZE VERSION DROPDOWNS
    # ---------------------------------------------------------
    def init_versions(self):
        versions = self.main.settings.settings["launcher"]["versions"].split(",")

        self.launcher.version_dropdown["values"] = versions
        self.launcher.version_var.set(self.main.settings.settings["launcher"]["version"])

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
