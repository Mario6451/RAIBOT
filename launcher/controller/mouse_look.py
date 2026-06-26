# controller/mouse_look.py

import math
from controller.bridge_comm import BridgeComm

class MouseLook:
    def __init__(self):
        self.bridge = BridgeComm()

    def look_toward(self, bot, target_x, target_z):
        dx = target_x - bot.x
        dz = target_z - bot.z

        angle = math.atan2(dz, dx)
        yaw = bot.yaw

        diff = angle - yaw

        # Normalize angle
        while diff > math.pi:
            diff -= 2 * math.pi
        while diff < -math.pi:
            diff += 2 * math.pi

        # Convert to mouse delta
        mouse_dx = diff * 50  # sensitivity

        self.bridge.camera_delta(mouse_dx, 0)
