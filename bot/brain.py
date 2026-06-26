import time
import random

from training import (
    TrainingConfig,
    TrainingMemory,
    ImitationLearning,
    InstructionLearning,
    RewardSystem,
    SkillStats,
    Learner
)

from ai.vision import VisionSystem
from ai.perception import PerceptionSystem
from ai.player_detector import PlayerDetector
from ai.chat_sniffer import ChatSniffer
from ai.movement import MovementController
from ai.state import BotState
from ai.personality import Personality
from ai.controller import InputController
from ai.camera import CameraController
from ai.chat import ChatSystem

from pathfinding import (
    make_flat_grid,
    MapScanner,
    AStar,
    PathMemory,
    DangerMap,
    world_to_grid,
    add_human_noise
)

from autoit_bridge import send_command, read_bot_state, wait_for_ready


class AIBrain:
    def __init__(self, bot_folder, settings, debug_callback=None):
        self.settings = settings
        self.debug = debug_callback or (lambda msg: None)

        self.training_config = TrainingConfig()
        self.training_config.self_learning_enabled = settings["training"]["self_learning"]
        self.training_config.imitation_learning_enabled = settings["training"]["imitation_learning"]
        self.training_config.instruction_learning_enabled = settings["training"]["instruction_learning"]

        self.memory = TrainingMemory(bot_folder)
        self.imitation = ImitationLearning(bot_folder)
        self.instruction = InstructionLearning(bot_folder)
        self.stats = SkillStats(bot_folder)
        self.rewarder = RewardSystem()
        self.learner = Learner(self.memory, self.stats, self.rewarder)

        self.state = BotState()
        self.movement = MovementController(self.stats)
        self.movement.state = self.state
        self.chat = ChatModule(settings)
        self.perception = PerceptionModule()

        grid_size = 20
        self.grid = make_flat_grid(grid_size)
        self.map_scanner = MapScanner(self.movement, self.state, grid_size=grid_size)
        self.path_memory = PathMemory(size=grid_size)
        self.danger_map = DangerMap(size=grid_size)

        self.current_path = []
        self.path_index = 0

        self.movement_style = self.imitation.get_movement_style()
        self.last_style_update = time.time()

        self.autoit_ready = False

        self.debug("AIBrain initialized (vision + pathfinding, no Roblox memory).")

    def update(self):
        now = time.time()

        if now - self.last_style_update > 10:
            self.movement_style = self.imitation.get_movement_style()
            self.last_style_update = now

        if not self.autoit_ready:
            if wait_for_ready(timeout=0.1):
                self.autoit_ready = True
                self.debug("[AIBrain] AutoIt connected.")
            else:
                return

        world = self.perception.capture()
        player = world.get("player")

        if player:
            px, _, pz = player["pos"]
            gx, gy = world_to_grid(px, pz, size=self.grid.shape[0])
            self.danger_map.mark(gx, gy, amount=2.0)
        self.danger_map.decay_step()

        if random.random() < 0.02:
            self.map_scanner.scan_step()
            self.grid = self.map_scanner.get_grid()

        action = self.decide_action(world)
        result = self.execute_action(action)

        if self.training_config.self_learning_enabled:
            self.learner.learn_from_action(action["type"], result)

        self._sync_autoit_state()

    def decide_action(self, world):
        cmd = world.get("chat_command")
        player = world.get("player")

        if cmd == "follow" and player:
            return {"type": "move_to_direct", "target": player["pos"]}
        if cmd == "stop":
            return {"type": "idle"}

        if world.get("chat_message"):
            msg = world["chat_message"]
            reply = self.chat.generate_reply(msg)
            return {"type": "chat", "text": reply}

        if player:
            if player["distance"] < 8:
                return {"type": "combat_move", "target": player}
            if random.random() < 0.15 * self.stats.awareness:
                return {"type": "circle_player", "target": player}
            if random.random() < 0.10:
                return {"type": "back_away", "target": player}

        if not self.current_path or self.path_index >= len(self.current_path):
            return self._plan_new_path()

        return {"type": "follow_path"}

    def _plan_new_path(self):
        target_world = self._random_point()

        gx_start, gy_start = world_to_grid(
            self.state.x, self.state.y,
            size=self.grid.shape[0]
        )
        gx_goal, gy_goal = world_to_grid(
            target_world[0], target_world[2],
            size=self.grid.shape[0]
        )

        astar = AStar(self.grid, danger_map=self.danger_map)
        path = astar.find_path((gx_start, gy_start), (gx_goal, gy_goal))

        path = self.path_memory.prefer_familiar(path)
        path = add_human_noise(path)

        self.current_path = path
        self.path_index = 0

        return {"type": "follow_path"}

    def execute_action(self, action):
        t = action["type"]

        if t == "chat":
            send_command("chat", {"text": action["text"]})
            return {"success": True}

        if t == "move_to_direct":
            x, y, z = action["target"]
            send_command("move_to", {
                "x": x, "y": y, "z": z,
                "style": self.movement_style
            })
            return {"success": True}

        if t == "follow_path":
            if not self.current_path or self.path_index >= len(self.current_path):
                return {"success": True}

            gx, gy = self.current_path[self.path_index]
            self.path_index += 1

            self.path_memory.mark(int(gx), int(gy))

            size = self.grid.shape[0]
            world_extent = 100.0
            wx = (gx / size) * world_extent - world_extent / 2
            wz = (gy / size) * world_extent - world_extent / 2

            send_command("move_to", {
                "x": wx,
                "y": 0,
                "z": wz,
                "style": self.movement_style
            })
            return {"success": True}

        if t == "explore":
            send_command("explore", {})
            return {"success": True}

        if t == "circle_player":
            x, y, z = action["target"]["pos"]
            send_command("circle_player", {"x": x, "y": y, "z": z})
            return {"success": True}

        if t == "back_away":
            x, y, z = action["target"]["pos"]
            send_command("back_away", {"x": x, "y": y, "z": z})
            return {"success": True}

        if t == "peek":
            send_command("peek", {})
            return {"success": True}

        if t == "combat_move":
            x, y, z = action["target"]["pos"]
            send_command("combat_move", {"x": x, "y": y, "z": z})
            return {"success": True}

        if t == "idle":
            return {"success": True}

        return {}

    def _sync_autoit_state(self):
        data = read_bot_state()
        if not data:
            return

        try:
            if "x" in data:
                self.state.x = float(data["x"])
            if "y" in data:
                self.state.y = float(data["y"])
            if "angle" in data:
                self.state.angle = float(data["angle"])
        except:
            pass

    def _random_point(self):
        return (
            random.uniform(-50, 50),
            random.uniform(0, 10),
            random.uniform(-50, 50)
        )
