# ai/personality_tactics.py
#
# Applies personality profile configs to bots.

from ai.personality_profiles import PersonalityRegistry

class PersonalityTactics:
    def __init__(self):
        self.registry = PersonalityRegistry()

    def apply_to_bot(self, bot):
        """
        Reads bot.personality_id and applies config to bot.
        """
        pid = getattr(bot, "personality_id", None)
        if pid is None:
            return

        profile = self.registry.get_profile(pid)
        if profile is None:
            return

        cfg = profile.config

        # Movement-related
        bot.speed_multiplier = cfg.get("speed_multiplier", 1.0)
        bot.wander_radius = cfg.get("wander_radius", 0)
        bot.random_detours = cfg.get("random_detours", False)
        bot.follow_distance = cfg.get("follow_distance", 0)
        bot.patrol_radius = cfg.get("patrol_radius", 0)

        # Combat / threat-related
        bot.attack_range = cfg.get("attack_range", 40)
        bot.fov = cfg.get("fov", 100)
        bot.retreat_threshold = cfg.get("retreat_threshold", 3)
        bot.avoid_open_areas = cfg.get("avoid_open_areas", False)
        bot.flank_preference = cfg.get("flank_preference", False)
        bot.hold_position = cfg.get("hold_position", False)

    def tick_world(self, world):
        """
        Optionally called each tick to ensure bots stay in sync
        with their personality configs.
        """
        for bot in world.bots:
            self.apply_to_bot(bot)
