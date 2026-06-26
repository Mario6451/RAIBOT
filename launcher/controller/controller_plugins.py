# launcher/controller/controller_plugins.py

import os


class PluginController:
    def __init__(self, main):
        self.main = main
        self.ui = main.ui

    def load_plugins(self):
        plugins_dir = "plugins"
        if not os.path.isdir(plugins_dir):
            self.ui.set_plugins([])
            return

        plugins = [f for f in os.listdir(plugins_dir) if f.endswith(".py")]
        self.ui.set_plugins(plugins)

    def enable_selected_plugin(self):
        sel = self.ui.plugin_list.curselection()
        if not sel:
            return
        plugin = self.ui.plugin_list.get(sel[0])
        self.ui.log_global(f"Enabled plugin: {plugin}")

    def disable_selected_plugin(self):
        sel = self.ui.plugin_list.curselection()
        if not sel:
            return
        plugin = self.ui.plugin_list.get(sel[0])
        self.ui.log_global(f"Disabled plugin: {plugin}")
