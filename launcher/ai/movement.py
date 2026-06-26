# movement.py
#
# Upgraded movement system using the new BridgeComm
# Supports:
# - KEY_DOWN / KEY_UP
# - mouse delta
# - mouse absolute
# - left/right click
# - jump
# - attack-move
# - formation movement
# - camera delta
#
# Fully compatible with the new AutoIt JSON command system.

from controller.bridge_comm import BridgeComm

bridge = BridgeComm()

# ============================================================
# BASIC KEY MOVEMENT
# ============================================================

def key_down(key: str) -> None:
    bridge.key_down(key)

def key_up(key: str) -> None:
    bridge.key_up(key)

def walk_forward() -> None:
    key_down("W")

def stop_forward() -> None:
    key_up("W")

def walk_backward() -> None:
    key_down("S")

def stop_backward() -> None:
    key_up("S")

def strafe_left() -> None:
    key_down("A")

def stop_strafe_left() -> None:
    key_up("A")

def strafe_right() -> None:
    key_down("D")

def stop_strafe_right() -> None:
    key_up("D")

def jump() -> None:
    key_down("SPACE")
    key_up("SPACE")

# ============================================================
# MOUSE ACTIONS
# ============================================================

def left_click() -> None:
    bridge.left_click()

def right_down() -> None:
    bridge.right_down()

def right_up() -> None:
    bridge.right_up()

def mouse_abs(x: int, y: int, speed: int = 0) -> None:
    bridge.mouse_abs(x, y, speed)

def mouse_delta(dx: int, dy: int) -> None:
    bridge.mouse_delta(dx, dy)

# ============================================================
# CAMERA CONTROL
# ============================================================

def camera_delta(dx: int, dy: int) -> None:
    """
    Move camera by dx/dy (yaw/pitch).
    """
    bridge.camera_delta(dx, dy)

# ============================================================
# AI BEHAVIOR COMMANDS
# ============================================================

def attack_move() -> None:
    """
    Attack-move behavior: AutoIt will right-click + move forward.
    """
    bridge.attack_move()

def formation_move(x: float, z: float) -> None:
    """
    Move bot to a formation offset target.
    """
    bridge.formation_move(x, z)

# ============================================================
# UTILITY
# ============================================================

def sleep(ms: int) -> None:
    bridge.sleep(ms)
