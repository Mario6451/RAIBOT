# ai/enemy_ai.py

import random
import math

class EnemyAI:
    def __init__(self, world, sensors):
        self.world = world
        self.sensors = sensors

    def tick(self, enemy):
        # If enemy sees a bot → chase
        target = self.sensors.get_closest_enemy(enemy)
        if target:
            self._chase(enemy, target)
            return

        # Otherwise patrol
        self._patrol(enemy)

    # ---------------------------------------------------------
    # PATROL
    # ---------------------------------------------------------
    def _patrol(self, enemy):
        if enemy.patrol_target is None:
            enemy.patrol_target = (
                enemy.x + random.randint(-30, 30),
                enemy.z + random.randint(-30, 30)
            )

        tx, tz = enemy.patrol_target
        dx = tx - enemy.x
        dz = tz - enemy.z

        dist = math.sqrt(dx*dx + dz*dz)
        if dist < 2:
            enemy.patrol_target = None
            return

        enemy.move_to(tx, tz)

    # ---------------------------------------------------------
    # CHASE
    # ---------------------------------------------------------
    def _chase(self, enemy, target):
        enemy.move_to(target.x, target.z)
