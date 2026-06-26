# ai/navmesh.py

import math
from typing import List, Tuple

class NavMesh:
    def __init__(self, triangles: List[List[Tuple[float, float]]]):
        self.triangles = triangles
        self.graph = self._build_graph()

    def _build_graph(self):
        graph = {}
        for i, tri_a in enumerate(self.triangles):
            graph[i] = []
            for j, tri_b in enumerate(self.triangles):
                if i == j:
                    continue
                if self._share_edge(tri_a, tri_b):
                    graph[i].append(j)
        return graph

    def _share_edge(self, a, b):
        shared = 0
        for p1 in a:
            for p2 in b:
                if abs(p1[0] - p2[0]) < 0.01 and abs(p1[1] - p2[1]) < 0.01:
                    shared += 1
        return shared >= 2

    def find_triangle(self, x, z):
        for i, tri in enumerate(self.triangles):
            if self._point_in_triangle((x, z), tri):
                return i
        return None

    def _point_in_triangle(self, p, tri):
        (x, y) = p
        (x1, y1), (x2, y2), (x3, y3) = tri

        denom = (y2 - y3)*(x1 - x3) + (x3 - x2)*(y1 - y3)
        a = ((y2 - y3)*(x - x3) + (x3 - x2)*(y - y3)) / denom
        b = ((y3 - y1)*(x - x3) + (x1 - x3)*(y - y3)) / denom
        c = 1 - a - b

        return 0 <= a <= 1 and 0 <= b <= 1 and 0 <= c <= 1

    def find_path(self, start, goal):
        start_tri = self.find_triangle(*start)
        goal_tri = self.find_triangle(*goal)

        if start_tri is None or goal_tri is None:
            return []

        # BFS on triangle graph
        queue = [start_tri]
        came_from = {start_tri: None}

        while queue:
            cur = queue.pop(0)
            if cur == goal_tri:
                break
            for nxt in self.graph[cur]:
                if nxt not in came_from:
                    came_from[nxt] = cur
                    queue.append(nxt)

        if goal_tri not in came_from:
            return []

        # Reconstruct triangle path
        tri_path = []
        node = goal_tri
        while node is not None:
            tri_path.append(node)
            node = came_from[node]
        tri_path.reverse()

        # Convert triangles → centroids
        world_path = []
        for tri_index in tri_path:
            tri = self.triangles[tri_index]
            cx = sum(p[0] for p in tri) / 3
            cz = sum(p[1] for p in tri) / 3
            world_path.append((cx, 0, cz))

        return world_path
