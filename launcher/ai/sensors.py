# ai/sensors.py

import math

class Sensors:
    def __init__(self, world):
        self.world = world  # world contains all bots, enemies, obstacles

    # Distance between two points
    def distance(self, x1, z1, x2, z2):
        return math.sqrt((x2 - x1)**2 + (z2 - z1)**2)

    # Get closest enemy within radius
    def get_closest_enemy(self, bot, radius=50):
        closest = None
        closest_dist = 999999

        for enemy in self.world.enemies:
            d = self.distance(bot.x, bot.z, enemy.x, enemy.z)
            if d < radius and d < closest_dist:
                closest = enemy
                closest_dist = d

        return closest

    # Field of view check
    def in_fov(self, bot, target, fov=90):
        dx = target.x - bot.x
        dz = target.z - bot.z

        angle_to_target = math.atan2(dz, dx)
        diff = abs(angle_to_target - bot.yaw)

        return diff < math.radians(fov / 2)

    # Line of sight (simple version)
    def has_los(self, bot, target):
        # No obstacles implemented yet — always true
        return True
