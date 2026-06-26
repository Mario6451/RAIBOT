# ui/edit_bot_panel.py

from ai.personality_profiles import PersonalityRegistry

class EditBotPanel:
    def __init__(self, world):
        self.world = world
        self.registry = PersonalityRegistry()
        self.selected_bot = None

    # ------------------------------
    # BOT SELECTION
    # ------------------------------
    def list_bots(self):
        return self.world.bots

    def select_bot(self, bot):
        self.selected_bot = bot

    # ------------------------------
    # PERSONALITY SELECTION
    # ------------------------------
    def list_personalities(self):
        return [
            (pid, profile.name)
            for pid, profile in self.registry.profiles.items()
        ]

    def assign_personality(self, personality_id: int):
        if self.selected_bot is None:
            return False

        if personality_id not in self.registry.profiles:
            return False

        self.selected_bot.personality_id = personality_id
        return True

    # ------------------------------
    # LOCK / UNLOCK PERSONALITY
    # ------------------------------
    def lock_personality(self, value: bool):
        if self.selected_bot:
            self.selected_bot.lock_personality = value
