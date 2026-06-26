# pathfinding/human_noise.py

import random


def add_human_noise(path):
    """
    Adds slight wobble, hesitation, and drift to make movement feel human.
    """
    noisy = []
    for (x, y) in path:
        nx = x + random.uniform(-0.2, 0.2)
        ny = y + random.uniform(-0.2, 0.2)

        if random.random() < 0.1:
            noisy.append((x, y))  # hesitation

        noisy.append((nx, ny))
    return noisy
