# ai/cover_system.py

import math

class CoverSystem:
    def __init__(self, world):
        self.world = world  # obstacles used as cover

    def find_cover_spots(self, bot, radius=40):
        spots = []
        for obs in self.world.obstacles:
            dx = obs["x"] - bot.x
            dz = obs["z"] - bot.z
            dist = math.sqrt(dx*dx + dz*dz)
            if dist < radius:
                # spot behind obstacle relative to enemy direction
                spots.append((obs["x"], 0, obs["z"]))
        return spots

    def best_cover(self, bot, enemy):
        spots = self.find_cover_spots(bot)
        if not spots:
            return None

        # pick farthest from enemy
        best = None
        best_dist = -1
        for (x, _, z) in spots:
            dx = x - enemy.x
            dz = z - enemy.z
            d = math.sqrt(dx*dx + dz*dz)
            if d > best_dist:
                best_dist = d
                best = (x, 0, z)
        return best
