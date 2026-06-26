# ai/navmesh_obstacles.py

class NavMeshObstacleIntegrator:
    def __init__(self, navmesh):
        self.navmesh = navmesh

    def carve_obstacle(self, x, z, radius):
        """
        Removes triangles that intersect with the obstacle.
        """
        new_tris = []
        for tri in self.navmesh.triangles:
            if self._triangle_far_from_circle(tri, x, z, radius):
                new_tris.append(tri)

        self.navmesh.triangles = new_tris
        self.navmesh.graph = self.navmesh._build_graph()

    def _triangle_far_from_circle(self, tri, ox, oz, r):
        for (x, z) in tri:
            if (x - ox)**2 + (z - oz)**2 < r*r:
                return False
        return True
