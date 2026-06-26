# pathfinding/danger_map.py

import numpy as np


class DangerMap:
    """
    Tracks danger intensity on the grid.
    Values decay over time.
    """

    def __init__(self, size=20, decay=0.95):
        self.map = np.zeros((size, size), dtype=np.float32)
        self.decay = decay

    def mark(self, gx, gy, amount=1.0):
        if 0 <= gx < self.map.shape[0] and 0 <= gy < self.map.shape[1]:
            self.map[gx, gy] += amount

    def decay_step(self):
        self.map *= self.decay

    def get(self, gx, gy):
        if 0 <= gx < self.map.shape[0] and 0 <= gy < self.map.shape[1]:
            return self.map[gx, gy]
        return 0.0
