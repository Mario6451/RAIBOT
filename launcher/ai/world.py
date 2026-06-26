# ai/world.py

class World:
    def __init__(self):
        self.bots = []
        self.enemies = []
        self.obstacles = []

    # ---------------------------------------------------------
    # BOT MANAGEMENT
    # ---------------------------------------------------------
    def add_bot(self, bot):
        self.bots.append(bot)

    def add_enemy(self, enemy):
        self.enemies.append(enemy)

    # ---------------------------------------------------------
    # OBSTACLES
    # ---------------------------------------------------------
    def add_obstacle(self, x, z, radius):
        self.obstacles.append({"x": x, "z": z, "radius": radius})

    # ---------------------------------------------------------
    # WORLD QUERY HELPERS
    # ---------------------------------------------------------
    def get_bot(self, name):
        for b in self.bots:
            if b.name == name:
                return b
        return None

    def get_enemies_in_radius(self, x, z, radius):
        result = []
        for e in self.enemies:
            dx = e.x - x
            dz = e.z - z
            if dx*dx + dz*dz <= radius*radius:
                result.append(e)
        return result
