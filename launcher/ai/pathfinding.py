import math
import random
import time
from typing import List, Tuple, Optional

from .state import AIState
from . import movement
from . import camera


class Pathfinder:
    """
    Lightweight human-like navigation:
    - move toward target
    - smooth turning
    - avoid stuck points
    - random wobble
    - simple path recalculation
    """

    def __init__(self):
        self.last_recalc = 0
        self.recalc_interval = 0.5
        self.turn_speed = 4
        self.walk_speed = 1

    # ---------------------------------------------------------
    # Main navigation entry point
    # ---------------------------------------------------------
    def navigate_to(self, state: AIState, target: Tuple[float, float, float]) -> None:
        """
        Move toward a world-space target (x, y, z).
        """
        if target is None:
            return

        tx, _, tz = target

        # Add slight human wobble
        wobble_x = tx + random.uniform(-0.2, 0.2)
        wobble_z = tz + random.uniform(-0.2, 0.2)

        # Convert to angle
        angle = math.degrees(math.atan2(wobble_z, wobble_x))

        # Turn camera toward target
        self._turn_toward_angle(state, angle)

        # Walk forward
        movement.walk_forward()
        state.movement.walking_forward = True
        state.mark_action()

    # ---------------------------------------------------------
    # Turning logic
    # ---------------------------------------------------------
    def _turn_toward_angle(self, state: AIState, angle: float) -> None:
        """
        Turn camera toward a desired yaw angle.
        """
        current_yaw = state.camera.yaw
        diff = angle - current_yaw

        # Normalize angle
        while diff > 180:
            diff -= 360
        while diff < -180:
            diff += 360

        # Apply smoothing
        step = max(min(diff, self.turn_speed), -self.turn_speed)

        # Update yaw
        state.camera.yaw += step

        # Convert yaw change to mouse delta
        camera.move_delta(int(step * 2), 0)
        state.camera.last_turn_time = time.time()

    # ---------------------------------------------------------
    # Stuck detection
    # ---------------------------------------------------------
    def check_stuck(self, state: AIState, movement_detected: bool) -> None:
        """
        Detect if bot is stuck and attempt recovery.
        """
        if movement_detected:
            state.clear_stuck()
            return

        # If no movement for too long → stuck
        if time.time() - state.last_action_time > 1.2:
            if not state.stuck:
                state.record_stuck((0, 0, 0))  # placeholder
            self._recover_from_stuck(state)

    def _recover_from_stuck(self, state: AIState) -> None:
        """
        Simple human-like recovery:
        - stop
        - back up
        - turn randomly
        - continue
        """
        movement.key_up("W")
        time.sleep(0.1)

        # Back up
        movement.key_down("S")
        time.sleep(0.2)
        movement.key_up("S")

        # Random turn
        turn = random.choice([-1, 1]) * random.randint(20, 60)
        camera.move_delta(turn, 0)

        state.clear_stuck()
        state.mark_action()

    # ---------------------------------------------------------
    # Path smoothing (simple)
    # ---------------------------------------------------------
    def smooth_path(self, path: List[Tuple[float, float, float]]) -> List[Tuple[float, float, float]]:
        """
        Simple smoothing: remove tiny zig-zags.
        """
        if len(path) < 3:
            return path

        smoothed = [path[0]]
        for i in range(1, len(path) - 1):
            x1, _, z1 = path[i - 1]
            x2, _, z2 = path[i]
            x3, _, z3 = path[i + 1]

            # If middle point is nearly straight, skip it
            angle1 = math.atan2(z2 - z1, x2 - x1)
            angle2 = math.atan2(z3 - z2, x3 - x2)

            if abs(angle1 - angle2) > 0.2:
                smoothed.append(path[i])

        smoothed.append(path[-1])
        return smoothed
