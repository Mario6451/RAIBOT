# ai/avoidance.py

import math

class Avoidance:
    def __init__(self, world):
        self.world = world

    def avoid(self, bot, target_x, target_z):
        for obs in self.world.obstacles:
            dx = obs["x"] - bot.x
            dz = obs["z"] - bot.z
            dist = math.sqrt(dx*dx + dz*dz)

            # If too close → push away
            if dist < obs["radius"] + 3:
                push_x = bot.x - obs["x"]
                push_z = bot.z - obs["z"]

                length = math.sqrt(push_x*push_x + push_z*push_z)
                if length == 0:
                    continue

                push_x /= length
                push_z /= length

                return (
                    bot.x + push_x * 5,
                    bot.z + push_z * 5
                )

        return (target_x, target_z)
