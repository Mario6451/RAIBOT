# ui/director_control_panel.py

from ai.ai_director import AIDirector

class DirectorControlPanel:
    def __init__(self, director: AIDirector):
        self.director = director

    # ------------------------------
    # ENABLE / DISABLE DIRECTOR
    # ------------------------------
    def set_enabled(self, value: bool):
        self.director.set_enabled(value)

    # ------------------------------
    # DIRECTOR MODES
    # ------------------------------
    def set_mode(self, mode: str):
        """
        mode: "dynamic", "calm", "intense", "custom"
        """
        self.director.set_mode(mode)

    # ------------------------------
    # DIFFICULTY & AGGRESSION
    # ------------------------------
    def set_difficulty(self, value: float):
        self.director.set_difficulty(value)

    def set_aggression(self, value: float):
        self.director.set_aggression(value)

    # ------------------------------
    # MANUAL TENSION OVERRIDE
    # ------------------------------
    def set_manual_tension(self, value: float):
        self.director.set_manual_tension(value)

    def clear_manual_override(self):
        self.director.clear_manual_override()

    # ------------------------------
    # FORCE PERSONALITY REASSIGNMENT
    # ------------------------------
    def reassign_all_personalities(self):
        self.director.assign_personalities_dynamic()
