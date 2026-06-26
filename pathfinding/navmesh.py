# pathfinding/navmesh.py

import numpy as np


def build_navmesh_from_grid(grid: np.ndarray):
    """
    Simple navmesh: list of walkable nodes.
    """
    h, w = grid.shape
    nodes = []
    for x in range(h):
        for y in range(w):
            if grid[x, y] == 0:
                nodes.append((x, y))
    return nodes
