import tkinter as tk
from tkinter import ttk

# -----------------------------
# Corrected Imports (Final)
# -----------------------------

# Main UI Tabs
from launcher.ai.ui.ui_launcher_tab import LauncherTab
from launcher.ai.ui.ui_bots_tab import BotsTab
from launcher.ai.ui.ui_avatar_converter_tab import AvatarConverterTab
from launcher.ai.ui.ui_logs_tab import AILogsTab
from launcher.ai.ui.ui_settings_tab import SettingsTab
from launcher.ai.ui.ui_plugins_tab import PluginsTab
from launcher.ai.ui.ui_process_tab import ProcessTab
from launcher.ai.ui.ui_window_tab import WindowTab
from launcher.ai.ui.ui_map_tab import MapTab
from launcher.ai.ui.ui_ai_tab import AITab

# AI Tabs
from launcher.ai.ui.ai.ai_command_tab import AICommandTab
from launcher.ai.ui.ai.bot_inspector_tab import BotInspectorTab
from launcher.ai.ui.ai.ai_logs_tab import AILogsTab as AILogsTab_AI
from launcher.ai.ui.ai.path_debug_tab import PathDebugTab
from launcher.ai.ui.ai.bot_manager_tab import BotManagerTab
from launcher.ai.ui.ai.ai_profiler_tab import AIProfilerTab

# Map
from launcher.ai.ui.map.ai_map_tab import AIMapTab

# Control Center Tabs
from launcher.ai.ui.edit_bot_tab import EditBotTab
from launcher.ai.ui.personality_editor_tab import PersonalityEditorTab
from launcher.ai.ui.director_control_tab import DirectorControlTab

# Panels
from launcher.ai.ui.edit_bot_panel import EditBotPanel
from launcher.ai.ui.personality_editor import PersonalityEditor
from launcher.ai.ui.director_control_panel import DirectorControlPanel


# -----------------------------
# Main UI Class
# -----------------------------

class MainUI(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Roblox AI Player - Launcher")
        self.geometry("1200x800")

        # Notebook (Tabs)
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True)

        # -----------------------------
        # Create Tabs
        # -----------------------------

        self.launcher_tab = LauncherTab(self.notebook)
        self.bots_tab = BotsTab(self.notebook)
        self.avatar_converter_tab = AvatarConverterTab(self.notebook)
        self.logs_tab = AILogsTab(self.notebook)
        self.settings_tab = SettingsTab(self.notebook)
        self.plugins_tab = PluginsTab(self.notebook)
        self.process_tab = ProcessTab(self.notebook)
        self.window_tab = WindowTab(self.notebook)
        self.map_tab = MapTab(self.notebook)
        self.ai_tab = AITab(self.notebook)

        # AI Tabs
        self.ai_command_tab = AICommandTab(self.notebook)
        self.bot_inspector_tab = BotInspectorTab(self.notebook)
        self.ai_logs_tab2 = AILogsTab_AI(self.notebook)
        self.path_debug_tab = PathDebugTab(self.notebook)
        self.bot_manager_tab = BotManagerTab(self.notebook)
        self.ai_profiler_tab = AIProfilerTab(self.notebook)

        # Control Center
        self.edit_bot_tab = EditBotTab(self.notebook)
        self.personality_editor_tab = PersonalityEditorTab(self.notebook)
        self.director_control_tab = DirectorControlTab(self.notebook)

        # -----------------------------
        # Add Tabs to Notebook
        # -----------------------------

        self.notebook.add(self.launcher_tab, text="Launcher")
        self.notebook.add(self.bots_tab, text="Bots")
        self.notebook.add(self.avatar_converter_tab, text="Avatar Converter")
        self.notebook.add(self.logs_tab, text="Logs")
        self.notebook.add(self.settings_tab, text="Settings")
        self.notebook.add(self.plugins_tab, text="Plugins")
        self.notebook.add(self.process_tab, text="Processes")
        self.notebook.add(self.window_tab, text="Window")
        self.notebook.add(self.map_tab, text="Map")
        self.notebook.add(self.ai_tab, text="AI")

        # AI Tabs
        self.notebook.add(self.ai_command_tab, text="AI Commands")
        self.notebook.add(self.bot_inspector_tab, text="Bot Inspector")
        self.notebook.add(self.ai_logs_tab2, text="AI Logs")
        self.notebook.add(self.path_debug_tab, text="Path Debug")
        self.notebook.add(self.bot_manager_tab, text="Bot Manager")
        self.notebook.add(self.ai_profiler_tab, text="AI Profiler")

        # Control Center
        self.notebook.add(self.edit_bot_tab, text="Edit Bot")
        self.notebook.add(self.personality_editor_tab, text="Personality Editor")
        self.notebook.add(self.director_control_tab, text="Director Control")


# -----------------------------
# Entry Point
# -----------------------------

if __name__ == "__main__":
    app = MainUI()
    app.mainloop()
