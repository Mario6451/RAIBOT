import random
import time
from typing import Dict, Any

from .state import AIState
from .pathfinding import Pathfinder
from . import movement
from . import camera


class AIBrain:
    """
    Core decision-making module.
    Reads perception → updates state → chooses action → executes movement.
    """

    def __init__(self):
        self.state = AIState()
        self.pathfinder = Pathfinder()
        self.last_behavior_update = 0
        self.behavior_interval = 0.2  # seconds

    # ---------------------------------------------------------
    # Main update loop (called every tick by bot_runtime)
    # ---------------------------------------------------------
    def update(self, world: Dict[str, Any]):
        now = time.time()

        # Update perception timestamps
        self.state.mark_perception()

        # Handle chat commands
        if world.get("chat_command"):
            self._handle_chat_command(world["chat_command"])

        # Handle player detection
        player = world.get("player")
        if player:
            self._handle_player_detection(player)

        # Stuck detection
        self.pathfinder.check_stuck(self.state, world.get("movement", False))

        # Behavior update
        if now - self.last_behavior_update > self.behavior_interval:
            self._decide_behavior()
            self.last_behavior_update = now

    # ---------------------------------------------------------
    # Chat command logic
    # ---------------------------------------------------------
    def _handle_chat_command(self, cmd: str):
        if cmd == "follow":
            self.state.behavior.mode = "follow"
        elif cmd == "stop":
            self.state.behavior.mode = "wander"

    # ---------------------------------------------------------
    # Player detection logic
    # ---------------------------------------------------------
    def _handle_player_detection(self, player: Dict[str, Any]):
        pos = player["pos"]
        dist = player["distance"]

        # Update target memory
        self.state.update_target_position(pos)

        # If in follow mode → follow player
        if self.state.behavior.mode == "follow":
            if dist > self.state.behavior.follow_distance:
                self.pathfinder.navigate_to(self.state, pos)
            else:
                movement.key_up("W")

        # If in chase mode → aggressive follow
        elif self.state.behavior.mode == "chase":
            self.pathfinder.navigate_to(self.state, pos)

    # ---------------------------------------------------------
    # Behavior decision logic
    # ---------------------------------------------------------
    def _decide_behavior(self):
        mode = self.state.behavior.mode

        if mode == "wander":
            self._wander_behavior()

        elif mode == "follow":
            # Follow behavior handled in player detection
            pass

        elif mode == "chase":
            # Chase handled in player detection
            pass

        elif mode == "sandbox":
            self._sandbox_behavior()

    # ---------------------------------------------------------
    # Wander behavior
    # ---------------------------------------------------------
    def _wander_behavior(self):
        """
        Simple human-like wandering:
        - randomly walk forward
        - randomly turn
        - occasionally stop
        """
        if random.random() < 0.02:
            # Random turn
            turn = random.choice([-1, 1]) * random.randint(10, 40)
            camera.move_delta(turn, 0)

        if random.random() < 0.05:
            # Start walking
            movement.walk_forward()
            self.state.movement.walking_forward = True

        if random.random() < 0.03:
            # Stop walking
            movement.key_up("W")
            self.state.movement.walking_forward = False

    # ---------------------------------------------------------
    # Sandbox behavior (everything enabled)
    # ---------------------------------------------------------
    def _sandbox_behavior(self):
        """
        Sandbox mode:
        - wander
        - follow if player detected
        - explore
        - random actions
        """
        # Random jump
        if random.random() < 0.01:
            movement.jump()

        # Random turn
        if random.random() < 0.02:
            camera.move_delta(random.randint(-20, 20), 0)

        # Random walk
        if random.random() < 0.05:
            movement.walk_forward()

        if random.random() < 0.03:
            movement.key_up("W")
