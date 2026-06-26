# pathfinding/obstacles.py

import numpy as np


def apply_dynamic_obstacles(grid: np.ndarray, obstacle_positions, danger_map=None):
    """
    obstacle_positions: hard-blocked tiles
    danger_map: optional DangerMap instance
    """

    # Hard obstacles
    for (gx, gy) in obstacle_positions:
        if 0 <= gx < grid.shape[0] and 0 <= gy < grid.shape[1]:
            grid[gx, gy] = 1

    # Soft danger (not blocked, but avoided)
    if danger_map is not None:
        danger = danger_map.map
        # Convert danger into soft-blocking
        # >0.5 danger → treat as blocked
        grid[danger > 0.5] = 1

    return grid
