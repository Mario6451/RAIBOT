# controller/auto_pathing.py

import math
from controller.movement_controller import MovementController

class AutoPathing:
    def __init__(self):
        self.move = MovementController()

    def walk_toward(self, bot, target_x, target_z):
        dx = target_x - bot.x
        dz = target_z - bot.z
        dist = math.sqrt(dx*dx + dz*dz)

        if dist < 1:
            self.move.stop_forward()
            return

        # Normalize direction
        nx = dx / dist
        nz = dz / dist

        # Forward/backward
        if nz > 0:
            self.move.walk_forward()
        else:
            self.move.walk_backward()

        # Strafing
        if nx > 0.2:
            self.move.strafe_right()
        elif nx < -0.2:
            self.move.strafe_left()
        else:
            self.move.stop_strafe_left()
            self.move.stop_strafe_right()
