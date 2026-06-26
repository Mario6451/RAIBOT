# ai/bot.py

import math

class Bot:
    def __init__(self, name, x=0, z=0):
        self.name = name

        # Position
        self.x = x
        self.z = z

        # Orientation
        self.yaw = 0.0

        # Movement
        self.path = []
        self.speed_multiplier = 1.0

        # Combat
        self.attack_range = 40
        self.fov = 90

        # Behavior mode
        self.mode = "normal"   # "normal", "attack_move"

        # Personality
        self.personality = "neutral"

        # Target (x, z)
        self.target = None

    # ---------------------------------------------------------
    # DISTANCE
    # ---------------------------------------------------------
    def distance_to(self, x, z):
        return math.sqrt((x - self.x)**2 + (z - self.z)**2)

    # ---------------------------------------------------------
    # UPDATE POSITION (called by movement systems)
    # ---------------------------------------------------------
    def update_position(self, new_x, new_z):
        self.x = new_x
        self.z = new_z

    # ---------------------------------------------------------
    # UPDATE YAW
    # ---------------------------------------------------------
    def update_yaw(self, yaw):
        self.yaw = yaw
