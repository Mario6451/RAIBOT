# ui/settings/__init__.py

from .general_tab import GeneralTab
from .llm_tab import LLMTab
from .training_tab import TrainingTab
from .performance_tab import PerformanceTab
from .training_stats_tab import TrainingStatsTab
from .debug_tab import DebugTab
from .settings_window import SettingsWindow

__all__ = [
    "GeneralTab",
    "LLMTab",
    "TrainingTab",
    "PerformanceTab",
    "TrainingStatsTab",
    "DebugTab",
    "SettingsWindow"
]
