# ai/path_visualizer.py

import pygame

class PathVisualizer:
    def __init__(self, surface, color=(0, 255, 0)):
        self.surface = surface
        self.color = color

    def draw_path(self, path):
        if len(path) < 2:
            return

        for i in range(len(path) - 1):
            x1, _, z1 = path[i]
            x2, _, z2 = path[i + 1]

            # Convert world → minimap coords