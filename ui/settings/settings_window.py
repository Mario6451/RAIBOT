# ui/settings/settings_window.py

import tkinter as tk
from tkinter import ttk
from settings import save_settings

# Import tab modules
from .general_tab import GeneralTab
from .llm_tab import LLMTab
from .training_tab import TrainingTab
from .performance_tab import PerformanceTab
from .training_stats_tab import TrainingStatsTab
from .debug_tab import DebugTab


class SettingsWindow:
    def __init__(self, root, settings):
        self.root = root
        self.settings = settings

        self._apply_auto_theme()
        self._apply_font()

        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill="both", expand=True)

        # Create tabs
        self.general_tab = GeneralTab(self.notebook, self.settings)
        self.llm_tab = LLMTab(self.notebook, self.settings)
        self.training_tab = TrainingTab(self.notebook, self.settings)
        self.performance_tab = PerformanceTab(self.notebook, self.settings)
        self.training_stats_tab = TrainingStatsTab(self.notebook)
        self.debug_tab = DebugTab(self.notebook)

        # Add tabs to notebook
        self.notebook.add(self.general_tab.frame, text="General")
        self.notebook.add(self.llm_tab.frame, text="LLM")
        self.notebook.add(self.training_tab.frame, text="Training")
        self.notebook.add(self.performance_tab.frame, text="Performance")
        self.notebook.add(self.training_stats_tab.frame, text="Training Stats")
        self.notebook.add(self.debug_tab.frame, text="AI Debug")

        # Save button
        ttk.Button(root, text="Save All Settings", command=self.save_all).pack(pady=10)

    # ---------------------------------------------------------
    # AUTO THEME + WINDOWS LOOK
    # ---------------------------------------------------------

    def _apply_auto_theme(self):
        style = ttk.Style()

        # Use system theme
        try:
            style.theme_use("vista")  # Windows-style tabs
        except:
            style.theme_use("default")

        # Auto light/dark based on OS
        # (ttk automatically adapts on Windows 10/11)

    def _apply_font(self):
        self.root.option_add("*Font", "Segoe UI 10")

    # ---------------------------------------------------------
    # SAVE ALL SETTINGS
    # ---------------------------------------------------------

    def save_all(self):
        # Save each tab
        self.general_tab.save()
        self.llm_tab.save()
        self.training_tab.save()
        self.performance_tab.save()

        # Write to disk
        save_settings(self.settings)
        print("[Settings] Saved successfully!")

    # ---------------------------------------------------------
    # DEBUG LOG (called by AIBrain)
    # ---------------------------------------------------------

    def debug_log(self, text):
        self.debug_tab.log(text)
