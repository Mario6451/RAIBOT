# ui/edit_bot_tab.py
#
# Logic for an "Edit Bot" tab where you assign personalities.
# You can hook this into any UI framework.

from ai.personality_profiles import PersonalityRegistry

class EditBotTab:
    def __init__(self, world):
        self.world = world
        self.registry = PersonalityRegistry()
        self.selected_bot = None

    def list_bots(self):
        return self.world.bots

    def select_bot(self, bot):
        self.selected_bot = bot

    def list_personalities(self):
        """
        Returns a list of (id, name) for UI dropdowns.
        """
        return [(pid, profile.name) for pid, profile in self.registry.profiles.items()]

    def assign_personality(self, personality_id: int):
        if self.selected_bot is None:
            return

        if personality_id not in self.registry.profiles:
            return

        self.selected_bot.personality_id = personality_id

    def create_custom_personality(self, slot_id: int, name: str, config: dict):
        """
        User-defined custom personality in slots 64–127.
        """
        self.registry.set_custom_profile(slot_id, name, config)
