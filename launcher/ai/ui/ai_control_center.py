# ai/ui/ai_control_center.py
#
# AI Control Center
# Combines:
# - Edit Bot Panel
# - Personality Editor
# - Director Control Panel
#
# This is the master UI logic layer for your launcher.

from ai.ui.edit_bot_panel import EditBotPanel
from ai.ui.personality_editor import PersonalityEditor
from ai.ui.director_control_panel import DirectorControlPanel

class AIControlCenter:
    def __init__(self, world, director):
        """
        world: your game world object
        director: instance of AIDirector
        """
        self.world = world
        self.director = director

        # Sub-panels
        self.edit_bot_panel = EditBotPanel(world)
        self.personality_editor = PersonalityEditor()
        self.director_panel = DirectorControlPanel(director)

        # UI state
        self.active_tab = "edit_bot"  # edit_bot, personality_editor, director

    # ---------------------------------------------------------
    # TAB SWITCHING
    # ---------------------------------------------------------
    def set_tab(self, tab_name: str):
        if tab_name in ["edit_bot", "personality_editor", "director"]:
            self.active_tab = tab_name

    # ---------------------------------------------------------
    # GET ACTIVE PANEL (for UI rendering)
    # ---------------------------------------------------------
    def get_active_panel(self):
        if self.active_tab == "edit_bot":
            return self.edit_bot_panel
        elif self.active_tab == "personality_editor":
            return self.personality_editor
        elif self.active_tab == "director":
            return self.director_panel

    # ---------------------------------------------------------
    # HIGH-LEVEL ACTIONS (UI buttons call these)
    # ---------------------------------------------------------
    def assign_personality_to_bot(self, bot, personality_id):
        self.edit_bot_panel.select_bot(bot)
        return self.edit_bot_panel.assign_personality(personality_id)

    def save_custom_personality(self, pid, name, config):
        return self.personality_editor.save_custom_profile(pid, name, config)

    def set_director_mode(self, mode):
        self.director_panel.set_mode(mode)

    def set_director_difficulty(self, value):
        self.director_panel.set_difficulty(value)

    def set_director_aggression(self, value):
        self.director_panel.set_aggression(value)

    def override_tension(self, value):
        self.director_panel.set_manual_tension(value)

    def clear_tension_override(self):
        self.director_panel.clear_manual_override()

    def reassign_all_personalities(self):
        self.director_panel.reassign_all_personalities()
