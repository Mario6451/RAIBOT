# pathfinding/grid.py

import numpy as np


def make_flat_grid(size=20):
    """
    0 = walkable
    1 = blocked
    """
    return np.zeros((size, size), dtype=np.int32)


def world_to_grid(x, z, size=20, world_extent=100.0):
    """
    Maps world (x,z) into grid coordinates.
    Assumes world spans roughly -50..+50 in both axes.
    Deterministic (no random jitter).
    """
    gx = int((x + world_extent / 2) / world_extent * size)
    gz = int((z + world_extent / 2) / world_extent * size)
    return gx, gz
