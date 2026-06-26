# ai/brain_movement.py

class MovementNode:
    """
    Behavior tree node for movement.
    Decides whether to:
    - follow a path
    - move toward a target
    - idle
    """

    def __init__(self, movement, sensors):
        self.movement = movement
        self.sensors = sensors

    def tick(self, bot):
        # If bot has a path → follow it
        if bot.path and len(bot.path) > 0:
            next_x, next_z = bot.path[0]

            # If close enough → pop waypoint
            if bot.distance_to(next_x, next_z) < 2:
                bot.path.pop(0)
                return

            # Move toward waypoint
            self.movement.move_to(next_x, next_z)
            return

        # If bot has a target → move toward it
        if bot.target:
            tx, tz = bot.target
            self.movement.move_to(tx, tz)
            return

        # Otherwise idle
        self.movement.key_up("W")
        self.movement.key_up("A")
        self.movement.key_up("S")
        self.movement.key_up("D")
