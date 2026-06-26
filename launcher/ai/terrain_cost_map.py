# ai/terrain_cost_map.py

class TerrainCostMap:
    def __init__(self, width, height, default_cost=1):
        self.width = width
        self.height = height
        self.cost = [[default_cost for _ in range(height)] for _ in range(width)]

    def set_cost(self, x, z, value):
        self.cost[x][z] = value

    def get_cost(self, x, z):
        return self.cost[x][z]

    def apply_to_astar(self, astar):
        """
        Modifies A* to use terrain costs.
        """
        original_neighbors = astar.neighbors

        def cost_neighbors(node):
            for nx, nz in original_neighbors(node):
                yield (nx, nz, self.cost[nx][nz])

        astar.neighbors = cost_neighbors
