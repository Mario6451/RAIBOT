# ai/ai_director.py
#
# Director AI v2 (clean version)
# - Tension system
# - Pacing system
# - Difficulty & aggression control
# - Dynamic personality assignment
# - Full manual override support
# - No debug overlay

import time
import random
from ai.personality_profiles import PersonalityRegistry

class AIDirector:
    def __init__(self, world):
        self.world = world
        self.registry = PersonalityRegistry()

        # Core director state
        self.tension = 0.0            # 0–10
        self.target_tension = 5.0     # desired tension
        self.difficulty = 1.0         # 0.5–2.0
        self.aggression = 1.0         # 0.5–2.0

        # Timing
        self.last_update = time.time()
        self.update_interval = 1.0

        # Control flags
        self.enabled = True
        self.manual_override = False
        self.mode = "dynamic"         # dynamic, calm, intense, custom

    # ---------------------------------------------------------
    # PUBLIC CONTROL API
    # ---------------------------------------------------------
    def set_enabled(self, value: bool):
        self.enabled = value

    def set_mode(self, mode: str):
        self.mode = mode

        if mode == "calm":
            self.target_tension = 2.0
        elif mode == "intense":
            self.target_tension = 8.0
        elif mode == "dynamic":
            self.target_tension = 5.0
        # custom mode leaves target_tension unchanged

    def set_difficulty(self, value: float):
        self.difficulty = max(0.5, min(2.0, value))

    def set_aggression(self, value: float):
        self.aggression = max(0.5, min(2.0, value))

    def set_manual_tension(self, value: float):
        self.manual_override = True
        self.tension = max(0.0, min(10.0, value))

    def clear_manual_override(self):
        self.manual_override = False

    # ---------------------------------------------------------
    # MAIN TICK
    # ---------------------------------------------------------
    def tick(self):
        if not self.enabled:
            return

        now = time.time()
        if now - self.last_update < self.update_interval:
            return

        self._update_tension()
        self._apply_pacing()
        self._dynamic_personality_assignment()

        self.last_update = now

    # ---------------------------------------------------------
    # 1) TENSION SYSTEM
    # ---------------------------------------------------------
    def _update_tension(self):
        if self.manual_override:
            return

        current = 0.0

        # Example tension metric: enemies near players
        for player in self.world.players:
            nearby = 0
            for enemy in self.world.enemies:
                dx = enemy.x - player.x
                dz = enemy.z - player.z
                if dx*dx + dz*dz < 40*40:
                    nearby += 1
            current += min(nearby, 10)

        if self.world.players:
            current /= len(self.world.players)

        # Smooth tension
        alpha = 0.3
        self.tension = (1 - alpha) * self.tension + alpha * current

        # Pull toward target tension
        beta = 0.1
        self.tension += (self.target_tension - self.tension) * beta

        self.tension = max(0.0, min(10.0, self.tension))

    # ---------------------------------------------------------
    # 2) PACING SYSTEM
    # ---------------------------------------------------------
    def _apply_pacing(self):
        if self.tension > 7.0:
            self.spawn_rate = 0.3 * self.difficulty
        elif self.tension > 4.0:
            self.spawn_rate = 0.6 * self.difficulty
        else:
            self.spawn_rate = 1.0 * self.difficulty

        self.attack_chance = 0.3 * self.aggression
        self.flank_chance = 0.2 * self.aggression

    # ---------------------------------------------------------
    # 3) DYNAMIC PERSONALITY ASSIGNMENT
    # ---------------------------------------------------------
    def _dynamic_personality_assignment(self):
        """
        Director assigns personalities based on tension.
        Bots with lock_personality=True are ignored.
        """
        for bot in self.world.bots:
            if getattr(bot, "lock_personality", False):
                continue

            if self.tension > 7.0:
                pid = self._pick_profile(["Aggressor", "Defender"])
            elif self.tension < 3.0:
                pid = self._pick_profile(["Explorer", "Social"])
            else:
                pid = self._pick_profile(
                    ["Aggressor", "Defender", "Explorer", "Social", "Guardian"]
                )

            if pid is not None:
                bot.personality_id = pid

    def _pick_profile(self, archetypes):
        candidates = [
            pid for pid, profile in self.registry.profiles.items()
            if profile.archetype in archetypes and pid < 64
        ]
        if not candidates:
            return None
        return random.choice(candidates)
