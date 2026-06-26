# controller/camera_controller.py
#
# Low-level camera control module.
# Sends yaw/pitch deltas to AutoIt via BridgeComm.
# Used by AI behaviors, auto-pathing, and mouse-look systems.

from controller.bridge_comm import BridgeComm
import math

class CameraController:
    def __init__(self):
        self.bridge = BridgeComm()

    # ---------------------------------------------------------
    # RAW CAMERA ROTATION
    # ---------------------------------------------------------
    def rotate(self, dx: float, dy: float):
        """
        Rotate camera by dx/dy mouse delta.
        Positive dx = turn right
        Positive dy = look down
        """
        self.bridge.camera_delta(dx, dy)

    # ---------------------------------------------------------
    # LOOK AT A WORLD POSITION
    # ---------------------------------------------------------
    def look_at(self, bot_x: float, bot_z: float, target_x: float, target_z: float, sensitivity: float = 50.0):
        """
        Smoothly rotate camera toward a world coordinate.
        Converts world-space direction into mouse delta.
        """

        dx = target_x - bot_x
        dz = target_z - bot_z

        # Angle to target
        angle = math.atan2(dz, dx)

        # Convert to degrees
        target_yaw = angle

        # AutoIt bot yaw is expected to be stored in bot.yaw
        # (Your AI brain should maintain this)
        # If not available, assume yaw = 0
        try:
            current_yaw = bot_yaw
        except:
            current_yaw = 0

        # Normalize angle difference
        diff = target_yaw - current_yaw
        while diff > math.pi:
            diff -= 2 * math.pi
        while diff < -math.pi:
            diff += 2 * math.pi

        # Convert yaw difference to mouse delta
        mouse_dx = diff * sensitivity

        # Send to AutoIt
        self.rotate(mouse_dx, 0)
