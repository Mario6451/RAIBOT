# ai/threat_analysis.py

import math

class ThreatAnalysis:
    def __init__(self, world):
        self.world = world

    def threat_level(self, bot):
        level = 0
        for enemy in self.world.enemies:
            dx = enemy.x - bot.x
            dz = enemy.z - bot.z
            dist = math.sqrt(dx*dx + dz*dz)

            if dist < 20:
                level += 3
            elif dist < 40:
                level += 2
            elif dist < 60:
                level += 1

        return level

    def recommend_action(self, bot):
        t = self.threat_level(bot)

        if t >= 6:
            return "retreat"
        elif t >= 3:
            return "take_cover"
        else:
            return "advance"
