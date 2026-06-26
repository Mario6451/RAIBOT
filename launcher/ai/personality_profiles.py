# ai/behavior_tree.py
#
# Full AI brain (v2):
# - sensors + combat
# - threat analysis
# - cover system
# - squad commands
# - hybrid navmesh + A*
# - human-like pathfinding
# - formation paths
# - terrain cost maps (optional hook)
# - multi-bot coordination
# - personality-based behavior

from ai.sensors import Sensors
from ai.combat import Combat
from ai.personality import Personality
from ai.pathfinding import Pathfinder, AStar
from ai.navmesh import NavMesh
from ai.navmesh_astar_hybrid import HybridPathfinder
from ai.formation_pathfinding import FormationPathfinder
from ai.cover_system import CoverSystem
from ai.threat_analysis import ThreatAnalysis
from ai.squad_commands import SquadCommandSystem
from ai.multi_bot_path_coordination import MultiBotCoordinator


class BehaviorTreeV2:
    def __init__(
        self,
        world,
        grid,
        navmesh_triangles,
        profiler=None
    ):
        # Core world + profiler
        self.world = world
        self.profiler = profiler

        # Core systems
        self.sensors = Sensors(world)
        self.movement_astar = AStar(grid)
        self.pathfinder = Pathfinder(grid)
        self.navmesh = NavMesh(navmesh_triangles)
        self.hybrid = HybridPathfinder(self.navmesh, grid)
        self.formation_pf = FormationPathfinder(self.hybrid)
        self.combat = Combat(self.pathfinder, self.sensors)
        self.personality = Personality(self.pathfinder)

        # Advanced systems
        self.cover = CoverSystem(world)
        self.threat = ThreatAnalysis(world)
        self.squad = SquadCommandSystem(world, self.formation_pf)
        self.coordinator = MultiBotCoordinator(world)

    # ---------------------------------------------------------
    # MAIN TICK
    # ---------------------------------------------------------
    def tick_world(self):
        # Optional: multi-bot coordination
        self.coordinator.adjust_paths()

        # Tick each bot
        for bot in self.world.bots:
            self.tick_bot(bot)

    def tick_bot(self, bot):
        # Apply personality (speed, FOV, attack range)
        self.personality.apply(bot)

        # Sense environment
        enemy = self.sensors.get_closest_enemy(bot)
        threat_level = self.threat.threat_level(bot)

        # Decide high-level mode
        self._decide_mode(bot, enemy, threat_level)

        # Execute behavior based on mode
        if bot.mode == "retreat":
            self._do_retreat(bot, enemy)
        elif bot.mode == "take_cover":
            self._do_take_cover(bot, enemy)
        elif bot.mode == "attack_move":
            self._do_attack_move(bot, enemy)
        elif bot.mode == "advance":
            self._do_advance(bot)
        else:
            self._do_idle(bot)

    # ---------------------------------------------------------
    # MODE DECISION
    # ---------------------------------------------------------
    def _decide_mode(self, bot, enemy, threat_level):
        if enemy is None:
            # No enemy → advance or idle
            if bot.target:
                bot.mode = "advance"
            else:
                bot.mode = "idle"
            return

        # Use threat analysis
        action = self.threat.recommend_action(bot)

        if action == "retreat":
            bot.mode = "retreat"
        elif action == "take_cover":
            bot.mode = "take_cover"
        else:
            # Safe enough → attack-move
            bot.mode = "attack_move"

    # ---------------------------------------------------------
    # RETREAT
    # ---------------------------------------------------------
    def _do_retreat(self, bot, enemy):
        if enemy is None:
            bot.mode = "idle"
            return

        # Run away from enemy
        dx = bot.x - enemy.x
        dz = bot.z - enemy.z

        # Normalize
        length = (dx**2 + dz**2) ** 0.5 or 1.0
        dx /= length
        dz /= length

        target_x = bot.x + dx * 20
        target_z = bot.z + dz * 20

        bot.target = (target_x, 0, target_z)
        self.pathfinder.navigate_to(bot.state, bot.target)
        self.pathfinder.check_stuck(bot.state, movement_detected=True)

    # ---------------------------------------------------------
    # TAKE COVER
    # ---------------------------------------------------------
    def _do_take_cover(self, bot, enemy):
        if enemy is None:
            bot.mode = "idle"
            return

        cover_spot = self.cover.best_cover(bot, enemy)
        if cover_spot is None:
            # No cover → fallback to retreat
            bot.mode = "retreat"
            self._do_retreat(bot, enemy)
            return

        bot.target = cover_spot
        self.pathfinder.navigate_to(bot.state, bot.target)
        self.pathfinder.check_stuck(bot.state, movement_detected=True)

    # ---------------------------------------------------------
    # ATTACK-MOVE
    # ---------------------------------------------------------
    def _do_attack_move(self, bot, enemy):
        if enemy:
            # Use combat system
            self.combat.tick(bot)
            return

        # No enemy → move toward target if any
        if bot.target:
            self.pathfinder.navigate_to(bot.state, bot.target)
            self.pathfinder.check_stuck(bot.state, movement_detected=True)
        else:
            bot.mode = "idle"

    # ---------------------------------------------------------
    # ADVANCE (non-combat movement)
    # ---------------------------------------------------------
    def _do_advance(self, bot):
        if not bot.target:
            bot.mode = "idle"
            return

        # Use hybrid navmesh + A*
        start = (bot.x, bot.z)
        goal = (bot.target[0], bot.target[2])

        path = self.hybrid.find_path(start, goal)
        if not path:
            # fallback to simple pathfinder
            self.pathfinder.navigate_to(bot.state, bot.target)
            return

        bot.path = path
        # Follow first waypoint
        if bot.path:
            wp = bot.path[0]
            self.pathfinder.navigate_to(bot.state, wp)
            self.pathfinder.check_stuck(bot.state, movement_detected=True)

    # ---------------------------------------------------------
    # IDLE
    # ---------------------------------------------------------
    def _do_idle(self, bot):
        # Stop movement
        bot.state.movement.walking_forward = False
        # Could add idle animations, scanning, etc.
        return

    # ---------------------------------------------------------
    # SQUAD COMMAND HOOKS
    # ---------------------------------------------------------
    def move_squad_to(self, squad_id, leader_start, leader_goal, formation_offsets):
        self.squad.move_squad(squad_id, leader_start, leader_goal, formation_offsets)

    def set_squad_mode(self, squad_id, mode):
        self.squad.set_squad_mode(squad_id, mode)
