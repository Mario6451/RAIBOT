# pathfinding/map_scanner.py

import numpy as np
import time
import random
import cv2

from ai.vision import Vision
from .grid import make_flat_grid, world_to_grid


class MapScanner:
    """
    Vision-only map scanner.
    Builds a walkable/blocked grid using:
        - human-like wandering
        - simple floor/obstacle segmentation
        - world_to_grid mapping
    """

    def __init__(self, movement, state, grid_size=20):
        self.movement = movement
        self.state = state
        self.vision = Vision()
        self.grid = make_flat_grid(grid_size)

        self.region = {
            "top": 350,
            "left": 500,
            "width": 280,
            "height": 200
        }

    def _mark_cell(self, gx, gy, walkable: bool):
        if 0 <= gx < self.grid.shape[0] and 0 <= gy < self.grid.shape[1]:
            self.grid[gx, gy] = 0 if walkable else 1

    def _capture_region(self):
        return self.vision.capture_region(self.region)

    def _detect_walkable(self, frame):
        if frame is None:
            return True

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 60, 120)

        edge_score = np.sum(edges) / 255
        brightness = np.mean(gray)

        if edge_score < 3000 and brightness > 40:
            return True
        return False

    def scan_step(self):
        frame = self._capture_region()
        walkable = self._detect_walkable(frame)

        me = self.state.self_pos
        gx, gy = world_to_grid(me["x"], me["z"], size=self.grid.shape[0])
        self._mark_cell(gx, gy, walkable)

    def explore_spiral(self, steps=40):
        for i in range(steps):
            self.movement._walk_human(random.uniform(0.3, 0.6))
            self.scan_step()

            if random.random() < 0.25:
                self.movement._camera_wiggle()

            time.sleep(random.uniform(0.1, 0.25))

    def get_grid(self):
        return self.grid
