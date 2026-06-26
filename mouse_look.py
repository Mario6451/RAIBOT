# mouse_look.py
# Smooth mouse-look for Roblox 2016 using right-click + relative movement
# No randomness, no jitter.

import ctypes
import time
from ctypes import wintypes

MOUSEEVENTF_MOVE       = 0x0001
MOUSEEVENTF_RIGHTDOWN  = 0x0008
MOUSEEVENTF_RIGHTUP    = 0x0010

class MouseInput(ctypes.Structure):
    _fields_ = [
        ("dx", wintypes.LONG),
        ("dy", wintypes.LONG),
        ("mouseData", wintypes.DWORD),
        ("dwFlags", wintypes.DWORD),
        ("time", wintypes.DWORD),
        ("dwExtraInfo", wintypes.ULONG_PTR),
    ]

class Input(ctypes.Structure):
    _fields_ = [
        ("type", wintypes.DWORD),
        ("mi", MouseInput),
    ]

SendInput = ctypes.windll.user32.SendInput


def _send_mouse(dx: int, dy: int, flags: int):
    inp = Input()
    inp.type = 0  # INPUT_MOUSE
    inp.mi = MouseInput(dx, dy, 0, flags, 0, 0)
    SendInput(1, ctypes.byref(inp), ctypes.sizeof(inp))


def right_down():
    _send_mouse(0, 0, MOUSEEVENTF_RIGHTDOWN)


def right_up():
    _send_mouse(0, 0, MOUSEEVENTF_RIGHTUP)


def move_relative(dx: int, dy: int):
    _send_mouse(dx, dy, MOUSEEVENTF_MOVE)


def smooth_move(dx: int, dy: int, duration: float = 0.12):
    """
    Smooth ease-in/ease-out movement, no randomness.
    """
    steps = int(duration * 60)
    if steps < 1:
        steps = 1

    for i in range(steps):
        t = i / steps
        ease = (1 - (2 * t - 1) ** 2)  # quadratic ease-in-out

        mx = int((dx * ease) / steps)
        my = int((dy * ease) / steps)

        move_relative(mx, my)
        time.sleep(1 / 120)


def look(dx: int, dy: int, smooth: bool = True):
    """
    Rotate camera like a real player by holding right-click.
    """
    right_down()

    if smooth:
        smooth_move(dx, dy)
    else:
        move_relative(dx, dy)

    right_up()


def toggle_first_person():
    """
    First-person toggle stub.
    Only call this when the AI learns a tool requires it.
    """
    import keyboard
    keyboard.press_and_release("shift")
