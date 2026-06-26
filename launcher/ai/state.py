import time
from dataclasses import dataclass, field
from typing import Optional, Tuple, List


@dataclass
class MovementState:
    walking_forward: bool = False
    walking_backward: bool = False
    strafing_left: bool = False
    strafing_right: bool = False
    jumping: bool = False
    last_move_time: float = field(default_factory=time.time)


@dataclass
class CameraState:
    holding_right: bool = False
    last_turn_time: float = field(default_factory=time.time)
    pitch: float = 0.0   # up/down
    yaw: float = 0.0     # left/right


@dataclass
class TargetState:
    target_player: Optional[str] = None
    target_position: Optional[Tuple[float, float, float]] = None
    last_seen_time: float = 0.0
    lost_target: bool = False


@dataclass
class NavigationMemory:
    visited_points: List[Tuple[float, float, float]] = field(default_factory=list)
    stuck_points: List[Tuple[float, float, float]] = field(default_factory=list)
    last_path: List[Tuple[float, float, float]] = field(default_factory=list)
    last_stuck_time: float = 0.0


@dataclass
class BehaviorSettings:
    mode: str = "wander"  # wander, follow, chase, sandbox
    awareness_radius: float = 25.0
    follow_distance: float = 6.0
    aggression: float = 0.0
    chat_frequency: float = 0.1
    reaction_speed: float = 0.2


@dataclass
class AIState:
    """Central AI memory container."""
    movement: MovementState = field(default_factory=MovementState)
    camera: CameraState = field(default_factory=CameraState)
    target: TargetState = field(default_factory=TargetState)
    nav: NavigationMemory = field(default_factory=NavigationMemory)
    behavior: BehaviorSettings = field(default_factory=BehaviorSettings)

    # general state
    last_action_time: float = field(default_factory=time.time)
    last_perception_update: float = 0.0
    stuck: bool = False
    stuck_counter: int = 0
    idle_since: float = field(default_factory=time.time)

    def mark_action(self):
        self.last_action_time = time.time()

    def mark_perception(self):
        self.last_perception_update = time.time()

    def record_visited(self, pos: Tuple[float, float, float]):
        self.nav.visited_points.append(pos)

    def record_stuck(self, pos: Tuple[float, float, float]):
        self.stuck = True
        self.stuck_counter += 1
        self.nav.stuck_points.append(pos)
        self.nav.last_stuck_time = time.time()

    def clear_stuck(self):
        self.stuck = False

    def set_target_player(self, name: str):
        self.target.target_player = name
        self.target.last_seen_time = time.time()
        self.target.lost_target = False

    def lose_target(self):
        self.target.lost_target = True
        self.target.target_player = None
        self.target.target_position = None

    def update_target_position(self, pos: Tuple[float, float, float]):
        self.target.target_position = pos
        self.target.last_seen_time = time.time()
        self.target.lost_target = False
