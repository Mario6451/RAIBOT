# pathfinding/smoothing.py

import random


def smooth_path(path, max_skip=2):
    if len(path) <= 2:
        return path

    smoothed = [path[0]]
    i = 0
    while i < len(path) - 1:
        jump = min(max_skip, len(path) - 1 - i)

        if random.random() < 0.2:
            jump = max(1, jump - 1)  # human-like corner overshoot

        smoothed.append(path[i + jump])
        i += jump

    return smoothed
