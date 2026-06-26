# launcher/controller/controller_settings.py

import json
import os
import ipaddress

SETTINGS_PATH = "settings.json"


class SettingsController:
    def __init__(self, main):
        self.main = main
        self.ui = main.ui
        self.settings = {}

    # ---------------------------------------------------------
    # Load settings (nested)
    # ---------------------------------------------------------
    def load(self):
        if not os.path.exists(SETTINGS_PATH):
            self.settings = {
                "web_ui": {
                    "enabled": True,
                    "ip": "0.0.0.0",
                    "port": 5000
                }
            }
        else:
            with open(SETTINGS_PATH, "r", encoding="utf8") as f:
                self.settings = json.load(f)

        flat = self.flatten(self.settings)
        self.ui.set_settings(flat)

    # ---------------------------------------------------------
    # Flatten / Unflatten
    # ---------------------------------------------------------
    def flatten(self, obj, prefix=""):
        flat = {}
        for k, v in obj.items():
            key = f"{prefix}.{k}" if prefix else k
            if isinstance(v, dict):
                flat.update(self.flatten(v, key))
            else:
                flat[key] = v
        return flat

    def unflatten(self, flat):
        nested = {}
        for key, value in flat.items():
            parts = key.split(".")
            d = nested
            for p in parts[:-1]:
                d = d.setdefault(p, {})
            d[parts[-1]] = value
        return nested

    # ---------------------------------------------------------
    # Save setting (with validation + auto‑restart Web‑UI)
    # ---------------------------------------------------------
    def save_setting(self):
        key = self.ui.settings_key_var.get().strip()
        val = self.ui.settings_value_var.get().strip()

        if not key:
            return

        # Validation
        if key == "web_ui.port":
            try:
                port = int(val)
                if not (1 <= port <= 65535):
                    raise ValueError
            except:
                self.ui.log_global("❌ Invalid port. Must be 1–65535.")
                return

        if key == "web_ui.ip":
            try:
                ipaddress.ip_address(val)
            except:
                self.ui.log_global("❌ Invalid IP address.")
                return

        # Convert types
        if val.isdigit():
            val = int(val)
        elif val.lower() in ("true", "false"):
            val = val.lower() == "true"

        # Update flattened
        flat = self.flatten(self.settings)
        flat[key] = val

        # Convert back to nested
        self.settings = self.unflatten(flat)

        # Save
        os.makedirs("settings", exist_ok=True)
        with open(SETTINGS_PATH, "w", encoding="utf8") as f:
            json.dump(self.settings, f, indent=4)

        # Update UI
        self.ui.set_settings(flat)

        # Restart Web‑UI if needed
        if key.startswith("web_ui."):
            self.main.webui.restart_server()

    # ---------------------------------------------------------
    # UI selection
    # ---------------------------------------------------------
    def on_setting_selected(self, event):
        sel = self.ui.settings_tree.selection()
        if not sel:
            return
        key, value = self.ui.settings_tree.item(sel[0], "values")
        self.ui.settings_key_var.set(key)
        self.ui.settings_value_var.set(str(value))
