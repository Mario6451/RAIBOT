# ai/behavior_tree.py
#
# Behavior Tree v3 — Full Integration
# - 128 personality profiles (8 archetypes × 8 subtypes + 64 custom)
# - Personality-driven tactics
# - Hybrid navmesh + A*
# - Cover system
# - Threat analysis
# - Squad logic
# - Multi-bot coordination
# - Sensors + combat
# - Movement + camera
# - World tick integration

from ai.sensors import Sensors
from ai.combat import Combat
from ai.personality_tactics import PersonalityTactics
from ai.pathfinding import Pathfinder, AStar
from ai.navmesh import NavMesh
from ai.navmesh_astar_hybrid import HybridPathfinder
from ai.formation_pathfinding import FormationPathfinder
from ai.cover_system import CoverSystem
from ai.threat_analysis import ThreatAnalysis
from ai.squad_commands import SquadCommandSystem
from ai.multi_bot_path_coordination import MultiBotCoordinator


class BehaviorTree:
    def __init__(self, world, grid, navmesh_triangles, profiler=None):
        self.world = world
        self.profiler = profiler

        # Core systems
        self.sensors = Sensors(world)
        self.combat = Combat(None, self.sensors)  # movement assigned later
        self.astar = AStar(grid)
        self.pathfinder = Pathfinder(grid)
        self.combat.pathfinder = self.pathfinder  # link movement to combat

        # Navigation
        self.navmesh = NavMesh(navmesh_triangles)
        self.hybrid = HybridPathfinder(self.navmesh, grid)
        self.formation_pf = FormationPathfinder(self.hybrid)

        # Advanced systems
        self.cover = CoverSystem(world)
        self.threat = ThreatAnalysis(world)
        self.squad = SquadCommandSystem(world, self.formation_pf)
        self.coordinator = MultiBotCoordinator(world)
        self.personality = PersonalityTactics()

    # ---------------------------------------------------------
    # WORLD TICK
    # ---------------------------------------------------------
    def tick_world(self):
        # Apply personality configs to all bots
        self.personality.tick_world(self.world)

        # Multi-bot coordination (avoid clumping)
        self.coordinator.adjust_paths()

        # Tick each bot
        for bot in self.world.bots:
            self.tick_bot(bot)

    # ---------------------------------------------------------
    # BOT TICK
    # ---------------------------------------------------------
    def tick_bot(self, bot):
        # Sense environment
        enemy = self.sensors.get_closest_enemy(bot)
        threat_level = self.threat.threat_level(bot)

        # Decide mode based on personality + threat
        self._decide_mode(bot, enemy, threat_level)

        # Execute behavior
        mode = bot.mode

        if mode == "retreat":
            self._do_retreat(bot, enemy)
        elif mode == "take_cover":
            self._do_take_cover(bot, enemy)
        elif mode == "attack_move":
            self._do_attack_move(bot, enemy)
        elif mode == "advance":
            self._do_advance(bot)
        else:
            self._do_idle(bot)

    # ---------------------------------------------------------
    # MODE DECISION
    # ---------------------------------------------------------
    def _decide_mode(self, bot, enemy, threat_level):
        if enemy is None:
            bot.mode = "advance" if bot.target else "idle"
            return

        # Personality-driven retreat threshold
        if threat_level >= bot.retreat_threshold:
            bot.mode = "retreat"
            return

        # Cover preference
        if bot.avoid_open_areas and threat_level >= 2:
            bot.mode = "take_cover"
            return

        # Flanking preference
        if bot.flank_preference and threat_level >= 1:
            bot.mode = "attack_move"
            return

        # Default combat mode
        bot.mode = "attack_move"

    # ---------------------------------------------------------
    # RETREAT
    # ---------------------------------------------------------
    def _do_retreat(self, bot, enemy):
        if enemy is None:
            bot.mode = "idle"
            return

        dx = bot.x - enemy.x
        dz = bot.z - enemy.z
        length = (dx*dx + dz*dz)**0.5 or 1
        dx /= length
        dz /= length

        bot.target = (bot.x + dx * 20, 0, bot.z + dz * 20)
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
            bot.mode = "retreat"
            return

        bot.target = cover_spot
        self.pathfinder.navigate_to(bot.state, bot.target)
        self.pathfinder.check_stuck(bot.state, movement_detected=True)

    # ---------------------------------------------------------
    # ATTACK-MOVE
    # ---------------------------------------------------------
    def _do_attack_move(self, bot, enemy):
        if enemy:
            self.combat.tick(bot)
            return

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

        start = (bot.x, bot.z)
        goal = (bot.target[0], bot.target[2])

        path = self.hybrid.find_path(start, goal)
        if not path:
            self.pathfinder.navigate_to(bot.state, bot.target)
            return

        bot.path = path

        if bot.path:
            wp = bot.path[0]
            self.pathfinder.navigate_to(bot.state, wp)
            self.pathfinder.check_stuck(bot.state, movement_detected=True)

    # ---------------------------------------------------------
    # IDLE
    # ---------------------------------------------------------
    def _do_idle(self, bot):
        bot.state.movement.walking_forward = False
        return

    # ---------------------------------------------------------
    # SQUAD COMMAND HOOKS
    # ---------------------------------------------------------
    def move_squad_to(self, squad_id, leader_start, leader_goal, formation_offsets):
        self.squad.move_squad(squad_id, leader_start, leader_goal, formation_offsets)

    def set_squad_mode(self, squad_id, mode):
        self.squad.set_squad_mode(squad_id, mode)
