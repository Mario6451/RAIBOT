"""
ui package initializer for RAIBOT

This file ensures that all UI modules can be imported cleanly, e.g.:

    from ui.settings_ui import SettingsUI
    from ui.launcher_ui import LauncherUI

It also exposes the most common UI classes at the package level.
"""

# Import UI modules so they are available as ui.SettingsUI, ui.LauncherUI, etc.
# These imports will not fail if optional modules are missing.

try:
    from .settings_ui import SettingsUI
except ImportError:
    SettingsUI = None

try:
    from .launcher_ui import LauncherUI
except ImportError:
    LauncherUI = None

try:
    from .window_ui import WindowUI
except ImportError:
    WindowUI = None

try:
    from .personality_ui import PersonalityUI
except ImportError:
    PersonalityUI = None

try:
    from .bot_manager_ui import BotManagerUI
except ImportError:
    BotManagerUI = None

# What the package exports
__all__ = [
    "SettingsUI",
    "LauncherUI",
    "WindowUI",
    "PersonalityUI",
    "BotManagerUI",
]
