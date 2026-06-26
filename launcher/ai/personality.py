# ai/personality.py

import random

class Personality:
    def __init__(self, movement):
        self.movement = movement

    def apply(self, bot):
        if bot.personality == "aggressive":
            self._aggressive(bot)
        elif bot.personality == "cautious":
            self._cautious(bot)
        elif bot.personality == "chaotic":
            self._chaotic(bot)

    # ---------------------------------------------------------
    # AGGRESSIVE
    # ---------------------------------------------------------
    def _aggressive(self, bot):
        bot.speed_multiplier = 1.3
        bot.attack_range = 60
        bot.fov = 120

    # ---------------------------------------------------------
    # CAUTIOUS
    # ---------------------------------------------------------
    def _cautious(self, bot):
        bot.speed_multiplier = 0.8
        bot.attack_range = 30
        bot.fov = 90

    # ---------------------------------------------------------
    # CHAOTIC
    # ---------------------------------------------------------
    def _chaotic(self, bot):
        bot.speed_multiplier = random.uniform(0.7, 1.4)
        bot.attack_range = random.randint(20, 80)
        bot.fov = random.randint(60, 160)
