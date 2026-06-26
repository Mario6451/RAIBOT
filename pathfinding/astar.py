# pathfinding/astar.py

import numpy as np
import heapq
import random


class AStar:
    def __init__(self, grid, danger_map=None):
        self.grid = grid
        self.danger_map = danger_map

    def heuristic(self, a, b):
        return np.linalg.norm(np.array(a) - np.array(b))

    def neighbors(self, node):
        x, y = node
        dirs = [
            (1, 0), (-1, 0), (0, 1), (0, -1),
            (1, 1), (1, -1), (-1, 1), (-1, -1)
        ]
        for dx, dy in dirs:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.grid.shape[0] and 0 <= ny < self.grid.shape[1]:
                if self.grid[nx, ny] == 0:
                    yield (nx, ny)

    def find_path(self, start, goal):
        pq = [(0, start)]
        came_from = {start: None}
        cost = {start: 0}

        while pq:
            _, current = heapq.heappop(pq)
            if current == goal:
                break

            for nxt in self.neighbors(current):
                base_cost = 1 + random.uniform(0.0, 0.3)

                # Add danger cost
                if self.danger_map:
                    gx, gy = nxt
                    base_cost += self.danger_map.get(gx, gy)

                new_cost = cost[current] + base_cost

                if nxt not in cost or new_cost < cost[nxt]:
                    cost[nxt] = new_cost
                    priority = new_cost + self.heuristic(goal, nxt)
                    heapq.heappush(pq, (priority, nxt))
                    came_from[nxt] = current

        # Reconstruct path
        path = []
        node = goal
        while node:
            path.append(node)
            node = came_from.get(node)
        path.reverse()
        return path
