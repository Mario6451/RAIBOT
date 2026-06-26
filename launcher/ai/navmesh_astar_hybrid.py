# ai/navmesh_astar_hybrid.py

from ai.navmesh import NavMesh
from ai.pathfinding import Pathfinder, AStar

class HybridPathfinder:
    """
    Hybrid navigation:
    - Navmesh for large-scale movement
    - A* grid for local precision
    - Human-like smoothing from Pathfinder
    """

    def __init__(self, navmesh: NavMesh, grid):
        self.navmesh = navmesh
        self.astar = AStar(grid)
        self.human = Pathfinder(grid)

    def find_path(self, start, goal):
        # 1) Navmesh path (triangle centroids)
        nav_path = self.navmesh.find_path(start, goal)
        if not nav_path:
            return []

        # 2) For each navmesh segment, refine with A*
        refined = []
        for i in range(len(nav_path) - 1):
            sx, _, sz = nav_path[i]
            gx, _, gz = nav_path[i + 1]

            sxg = int(sx // 4)
            szg = int(sz // 4)
            gxg = int(gx // 4)
            gzg = int(gz // 4)

            local = self.astar.find_path((sxg, szg), (gxg, gzg))
            for lx, lz in local:
                refined.append((lx * 4, 0, lz * 4))

        # 3) Human-like smoothing
        return self.human.smooth_path(refined)
