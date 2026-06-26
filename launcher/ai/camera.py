import socket

AUTOIT_HOST = "127.0.0.1"
AUTOIT_PORT = 5005

def _send(cmd: str) -> None:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((AUTOIT_HOST, AUTOIT_PORT))
    s.send(cmd.encode("utf-8"))
    s.close()

# --- right-click camera control ---

def hold_right() -> None:
    _send("MOUSE_RIGHT_DOWN")

def release_right() -> None:
    _send("MOUSE_RIGHT_UP")

def move_delta(dx: int, dy: int) -> None:
    _send(f"MOUSE_MOVE_DELTA|{dx}|{dy}")

def move_abs(x: int, y: int, speed: int = 1) -> None:
    _send(f"MOUSE_MOVE_ABS|{x}|{y}|{speed}")

# --- higher-level camera helpers ---

def turn_right(pixels: int) -> None:
    move_delta(pixels, 0)

def turn_left(pixels: int) -> None:
    move_delta(-pixels, 0)

def look_up(pixels: int) -> None:
    move_delta(0, -pixels)

def look_down(pixels: int) -> None:
    move_delta(0, pixels)
