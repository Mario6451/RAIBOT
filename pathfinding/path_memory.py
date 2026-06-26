# pathfinding/path_memory.py

import numpy as np


class PathMemory:
    def __init__(self, size=20):
        self.heatmap = np.zeros((size, size), dtype=np.float32)

    def mark(self, gx, gy):
        if 0 <= gx < self.heatmap.shape[0] and 0 <= gy < self.heatmap.shape[1]:
            self.heatmap[gx, gy] += 1.0

    def prefer_familiar(self, path):
        """
        Reorders path slightly to prefer familiar tiles.
        """
        scored = []
        h, w = self.heatmap.shape

        for (x, y) in path:
            ix, iy = int(x), int(y)
            if 0 <= ix < h and 0 <= iy < w:
                score = self.heatmap[ix, iy]
            else:
                score = 0.0
            scored.append((score, (x, y)))

        scored.sort(reverse=True, key=lambda t: t[0])
        return [p for (_, p) in scored]
