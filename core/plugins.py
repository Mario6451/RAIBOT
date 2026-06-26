import os
import importlib

PLUGIN_DIR = os.path.join(os.path.dirname(__file__), "..", "plugins")

class Plugin:
    def __init__(self, name, module, enabled=True):
        self.name = name
        self.module = module
        self.enabled = enabled
        self.description = getattr(module, "DESCRIPTION", "No description provided.")

def load_plugins():
    plugins = []
    for file in os.listdir(PLUGIN_DIR):
        if file.endswith(".py"):
            name = file[:-3]
            try:
                module = importlib.import_module(f"plugins.{name}")
                plugins.append(Plugin(name, module))
            except Exception as e:
                print(f"[PLUGIN ERROR] Failed to load {file}: {e}")
    return plugins

PLUGINS = load_plugins()
