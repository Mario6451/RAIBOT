# ui/personality_editor.py

from ai.personality_profiles import PersonalityRegistry

class PersonalityEditor:
    def __init__(self):
        self.registry = PersonalityRegistry()

    # ------------------------------
    # CUSTOM PERSONALITY SLOTS
    # ------------------------------
    def list_custom_slots(self):
        return [
            (pid, profile.name)
            for pid, profile in self.registry.profiles.items()
            if 64 <= pid <= 127
        ]

    def load_profile(self, pid: int):
        return self.registry.get_profile(pid)

    # ------------------------------
    # SAVE CUSTOM PERSONALITY
    # ------------------------------
    def save_custom_profile(self, pid: int, name: str, config: dict):
        if pid < 64 or pid > 127:
            return False

        self.registry.set_custom_profile(pid, name, config)
        return True
