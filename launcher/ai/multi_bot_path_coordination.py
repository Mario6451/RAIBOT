# ai/multi_bot_path_coordination.py

import math

class MultiBotCoordinator:
    def __init__(self, world):
        self.world = world

    def adjust_paths(self):
        bots = self.world.bots

        for i in range(len(bots)):
            for j in range(i + 1, len(bots)):
                b1 = bots[i]
                b2 = bots[j]

                dx = b2.x - b1.x
                dz = b2.z - b1.z
                dist = math.sqrt(dx*dx + dz*dz)

                if dist < 3:
                    # Push them apart
                    push_x = dx / dist
                    push_z = dz / dist

                    b1.x -= push_x * 0.5
                    b1.z -= push_z * 0.5

                    b2.x += push_x * 0.5
                    b2.z += push_z * 0.5
