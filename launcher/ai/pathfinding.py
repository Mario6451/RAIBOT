import math
import random
import time
import heapq
from typing import List, Tuple, Optional

from .state import AIState
from . import movement
from . import camera


# ============================================================
# A* GRID PATHFINDING
# ============================================================

class AStar:
    def __init__(self, grid):
        self.grid = grid  # 2D array: 0 = walkable, 1 = blocked

    def heuristic(self, a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def neighbors(self, node):
        x, z = node
        dirs = [(1,0), (-1,0), (0,1), (0,-1)]
        for dx, dz in dirs:
            nx, nz = x + dx, z + dz
            if 0 <= nx < len(self.grid) and 0 <= nz < len(self.grid[0]):
                if self.grid[nx][nz] == 0:
                    yield (nx, nz)

    def find_path(self, start, goal):
        frontier = []
        heapq.heappush(frontier, (0, start))

        came_from = {start: None}
        cost = {start: 0}

        while frontier:
            _, current = heapq.heappop(frontier)

            if current == goal:
                break

            for next_node in self.neighbors(current):
                new_cost = cost[current] + 1
                if next_node not in cost or new_cost < cost[next_node]:
                    cost[next_node] = new_cost
                    priority = new_cost + self.heuristic(goal, next_node)
                    heapq.heappush(frontier, (priority, next_node))
                    came_from[next_node] = current

        if goal not in came_from:
            return []

        # Reconstruct path
        path = []
        node = goal
        while node:
            path.append(node)
            node = came_from[node]

        path.reverse()
        return path


# ============================================================
# HUMAN-LIKE PATH FOLLOWING
# ============================================================

class Pathfinder:
    """
    Unified pathfinding system:
    - A* grid pathfinding
    - path smoothing
    - human-like wobble
    - smooth turning
    - stuck detection + recovery
    """

    def __init__(self, grid):
        self.astar = AStar(grid)
        self.last_recalc = 0
        self.recalc_interval = 0.5
        self.turn_speed = 4
        self.walk_speed = 1
        self.current_path = []

    # ---------------------------------------------------------
    # Compute A* path and smooth it
    # ---------------------------------------------------------
    def compute_path(self, start: Tuple[int,int], goal: Tuple[int,int]):
        raw = self.astar.find_path(start, goal)
        if not raw:
            return []

        # Convert grid coords → world coords
        world_path = [(x * 4, 0, z * 4) for (x, z) in raw]

        return self.smooth_path(world_path)

    # ---------------------------------------------------------
    # Main navigation entry point
    # ---------------------------------------------------------
    def navigate_to(self, state: AIState, target: Tuple[float, float, float]) -> None:
        if target is None:
            return

        # Recalculate A* path every 0.5s
        now = time.time()
        if now - self.last_recalc > self.recalc_interval or not self.current_path:
            sx = int(state.position.x // 4)
            sz = int(state.position.z // 4)
            gx = int(target[0] // 4)
            gz = int(target[2] // 4)

            self.current_path = self.compute_path((sx, sz), (gx, gz))
            self.last_recalc = now

        if not self.current_path:
            return

        # Follow next waypoint
        wx, _, wz = self.current_path[0]

        # If close → pop waypoint
        if state.distance_to(wx, wz) < 2:
            self.current_path.pop(0)
            return

        # Add slight human wobble
        wobble_x = wx + random.uniform(-0.2, 0.2)
        wobble_z = wz + random.uniform(-0.2, 0.2)

        # Convert to angle
        angle = math.degrees(math.atan2(wobble_z - state.position.z,
                                        wobble_x - state.position.x))

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
        if movement_detected:
            state.clear_stuck()
            return

        if time.time() - state.last_action_time > 1.2:
            if not state.stuck:
                state.record_stuck((0, 0, 0))
            self._recover_from_stuck(state)

    def _recover_from_stuck(self, state: AIState) -> None:
        movement.key_up("W")
        time.sleep(0.1)

        movement.key_down("S")
        time.sleep(0.2)
        movement.key_up("S")

        turn = random.choice([-1, 1]) * random.randint(20, 60)
        camera.move_delta(turn, 0)

        state.clear_stuck()
        state.mark_action()

    # ---------------------------------------------------------
    # Path smoothing
    # ---------------------------------------------------------
    def smooth_path(self, path: List[Tuple[float, float, float]]):
        if len(path) < 3:
            return path

        smoothed = [path[0]]
        for i in range(1, len(path) - 1):
            x1, _, z1 = path[i - 1]
            x2, _, z2 = path[i]
            x3, _, z3 = path[i + 1]

            angle1 = math.atan2(z2 - z1, x2 - x1)
            angle2 = math.atan2(z3 - z2, x3 - x2)

            if abs(angle1 - angle2) > 0.2:
                smoothed.append(path[i])

        smoothed.append(path[-1])
        return smoothed
