import os
from launcher.features.avatar_converter import convert_rblxhub_to_legacy, convert_to_sigmabinary
from launcher.features.version_manager import get_version_info

class AvatarConverterController:
    def __init__(self, main):
        self.main = main
        self.ui = main.ui.avatar_converter

    def convert_avatar(self):
        path = self.ui.avatar_path_var.get()
        version = self.ui.version_var.get()

        if not os.path.exists(path):
            self.ui.show_preview("Invalid avatar.ini path.")
            return

        legacy = convert_rblxhub_to_legacy(path)
        info = get_version_info(self.main.settings.settings, version)

        if info["avatar_system"] == "sigmabinary":
            legacy["binary"] = convert_to_sigmabinary(legacy)

        preview = "\n".join([f"{k}={v}" for k, v in legacy.items()])
        self.ui.show_preview(preview)

        self.converted_data = legacy

    def save_converted_avatar(self):
        if not hasattr(self, "converted_data"):
            self.ui.show_preview("Nothing to save.")
            return

        bot_name = self.main.ui.launcher.bot_selector.get()
        if not bot_name:
            self.ui.show_preview("No bot selected.")
            return

        folder = os.path.join("bots", bot_name)
        os.makedirs(folder, exist_ok=True)

        with open(os.path.join(folder, "avatar.ini"), "w") as f:
            f.write("[Avatar]\n")
            for k, v in self.converted_data.items():
                f.write(f"{k}={v}\n")

        self.ui.show_preview("Saved to bot successfully.")
