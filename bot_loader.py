# bot_loader.py

import os
import configparser


def load_bot_profile(bot_folder: str):
    """
    Loads a bot profile from:
        bots/<BotName>/user.ini

    Returns a dict with all settings.
    """

    ini_path = os.path.join("bots", bot_folder, "user.ini")

    if not os.path.exists(ini_path):
        raise FileNotFoundError(f"[bot_loader] user.ini not found: {ini_path}")

    config = configparser.ConfigParser()
    config.read(ini_path, encoding="utf8")

    profile = {}

    # Convert INI sections → dict
    for section in config.sections():
        profile[section] = {}
        for key, value in config.items(section):
            # Auto‑convert numbers
            if value.isdigit():
                value = int(value)
            else:
                try:
                    value = float(value)
                except:
                    pass
            profile[section][key] = value

    return profile
