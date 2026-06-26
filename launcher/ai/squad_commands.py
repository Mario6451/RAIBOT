# ai/squad_commands.py

class SquadCommandSystem:
    def __init__(self, world, formation_pathfinder):
        self.world = world
        self.formation_pathfinder = formation_pathfinder

    def get_squad(self, squad_id):
        return [b for b in self.world.bots if getattr(b, "squad_id", None) == squad_id]

    def move_squad(self, squad_id, leader_start, leader_goal, formation_offsets):
        squad = self.get_squad(squad_id)
        if not squad:
            return

        paths = self.formation_pathfinder.find_formation_paths(
            leader_start, leader_goal, formation_offsets
        )
        for bot, path in zip(squad, paths):
            bot.path = path

    def set_squad_mode(self, squad_id, mode):
        for b in self.get_squad(squad_id):
            b.mode = mode
