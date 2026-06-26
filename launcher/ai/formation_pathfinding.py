# ai/formation_pathfinding.py

import math

class FormationPathfinder:
    def __init__(self, base_pathfinder):
        self.base = base_pathfinder

    def assign_offsets(self, formation_offsets, leader_path):
        """
        Given a leader path and formation offsets,
        generate paths for each bot.
        """
        bot_paths = []

        for offset in formation_offsets:
            ox, oz = offset
            bot_path = []

            for (x, _, z) in leader_path:
                bot_path.append((x + ox, 0, z + oz))

            bot_paths.append(bot_path)

        return bot_paths

    def find_formation_paths(self, leader_start, leader_goal, formation_offsets):
        leader_path = self.base.find_path(leader_start, leader_goal)
        if not leader_path:
            return []

        return self.assign_offsets(formation_offsets, leader_path)
