# ui/settings/settings_window.py

import tkinter as tk
from tkinter import ttk
from settings import save_settings

# Import tab modules
from .general_tab import GeneralTab
from .llm_tab import LLMTab
from .performance_tab import PerformanceTab
from .debug_tab import DebugTab

# NEW TABS
from .ai_behavior_tab import AIBehaviorTab
from .ai_performance_tab import AIPerformanceTab


class SettingsWindow:
    def __init__(self, root, settings, controller_ai=None, controller_bots=None):
        self.root = root
        self.settings = settings
        self.controller_ai = controller_ai
        self.controller_bots = controller_bots

        self._apply_auto_theme()
        self._apply_font()

        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill="both", expand=True)

        # Create tabs
        self.general_tab = GeneralTab(self.notebook, self.settings)
        self.llm_tab = LLMTab(self.notebook, self.settings)
        self.performance_tab = PerformanceTab(self.notebook, self.settings)

        # NEW AI TABS
        self.ai_behavior_tab = AIBehaviorTab(self.notebook, controller_ai)
        self.ai_performance_tab = AIPerformanceTab(self.notebook, controller_ai)

        self.debug_tab = DebugTab(self.notebook)

        # Add tabs to notebook
        self.notebook.add(self.general_tab.frame, text="General")
        self.notebook.add(self.llm_tab.frame, text="LLM")
        self.notebook.add(self.performance_tab.frame, text="Performance")

        # NEW TAB LABELS
        self.notebook.add(self.ai_behavior_tab, text="AI Behavior")
        self.notebook.add(self.ai_performance_tab, text="AI Performance")

        self.notebook.add(self.debug_tab.frame, text="AI Debug")

        # Save button
        ttk.Button(root, text="Save All Settings", command=self.save_all).pack(pady=10)

    # ---------------------------------------------------------
    # AUTO THEME + WINDOWS LOOK
    # ---------------------------------------------------------

    def _apply_auto_theme(self):
        style = ttk.Style()
        try:
            style.theme_use("vista")
        except:
            style.theme_use("default")

    def _apply_font(self):
        self.root.option_add("*Font", "Segoe UI 10")

    # ---------------------------------------------------------
    # SAVE ALL SETTINGS
    # ---------------------------------------------------------

    def save_all(self):
        self.general_tab.save()
        self.llm_tab.save()
        self.performance_tab.save()

        save_settings(self.settings)
        print("[Settings] Saved successfully!")

    # ---------------------------------------------------------
    # DEBUG LOG
    # ---------------------------------------------------------

    def debug_log(self, text):
        self.debug_tab.log(text)
