import json
import os

SETTINGS_FILE = os.path.join(os.path.dirname(__file__), "settings.json")

DEFAULT_SETTINGS = {
    "general": {
        "bot_name": "RAI Bot",                 # from weak root
        "client_path": "",                    # from weak root
        "auto_launch": False,                 # from both
        "model": "microsoft/phi-4-mini-reasoning",   # from strong core
        "model_endpoint": "http://localhost:1234/v1/chat/completions",  # from strong core
        "default_exe_path": "",               # from strong core
        "default_avatar": ""                  # from strong core
    },

    "llm": {
        "temperature": 0.8,                   # from strong core
        "max_tokens": 4096,                   # from strong core
        "system_prompt": (                    # from strong core
            "You are a Roblox player in the year 2016. You talk exactly like real Roblox kids from that era. "
            "Your grammar is casual, messy, and sometimes incorrect. You use short messages, quick reactions, "
            "and simple words. You never use emojis, modern slang, or anything that didn’t exist in 2016. "
            "Your personality is friendly, chaotic, energetic, and easily excited. You say things like lol, xd, "
            "bruh, omg, wow, rip, rekt, pls, thx, noob. You sometimes trash-talk but only in a playful way. "
            "You act like a normal 2016 kid, not an adult. "
            "Your chat style: short messages (1–8 words), no emojis, no modern slang (no fr, cap, gyatt, rizz, etc.), "
            "only 2016 slang. Use simple reactions like 'lol what', 'wait', 'hold up', 'bro', 'wow', 'no way'. "
            "Behavior rules: stay in character as a 2016 Roblox player at all times, never mention AI, models, or anything modern. "
            "If someone insults you, respond like a 2016 kid (lol ok, bruh, no u, xd). "
            "If someone asks for help, respond simply (ok, coming, where u at). "
            "If someone says something confusing, respond like a kid (huh, what u mean). "
            "Movement/action interpretation: if someone says follow me, come here, attack him, jump, run, help, stop, wait, "
            "interpret them as in-game actions and respond with short confirmations like ok, coming, wait, on my way, k, hold up. "
            "Tone: casual, playful, slightly chaotic, never too serious, never too mature, never too modern. "
            "Always speak like a real 2016 Roblox player."
        )
    },

    "training": {
        "self_learning": True,                # from both
        "imitation_learning": True,           # from both
        "instruction_learning": True          # from both
    },

    "performance": {
        "tick_rate": 20,                      # from weak root
        "capture_fps": 12,                    # from strong core
        "pathfinding_grid_size": 64,          # from strong core
        "logging_enabled": True               # from strong core
    }
}


def _merge_defaults(current, default):
    for key, value in default.items():
        if key not in current:
            current[key] = value
        elif isinstance(value, dict):
            current[key] = _merge_defaults(current[key], value)
    return current


def load_settings():
    if not os.path.exists(SETTINGS_FILE):
        save_settings(DEFAULT_SETTINGS)
        return DEFAULT_SETTINGS

    try:
        with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)

        merged = _merge_defaults(data, DEFAULT_SETTINGS)
        save_settings(merged)
        return merged

    except Exception as e:
        print(f"[Settings] Failed to load settings: {e}")
        return DEFAULT_SETTINGS


def save_settings(settings):
    try:
        with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
            json.dump(settings, f, indent=4)
    except Exception as e:
        print(f"[Settings] Failed to save settings: {e}")


SETTINGS = load_settings()
