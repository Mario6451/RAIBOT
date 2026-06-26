import json
import time
import subprocess
import os


def send_command(cmd, data=None):
    if data is None:
        data = {}
    payload = json.dumps({"cmd": cmd, "data": data})
    # TODO: write to your existing pipe/file/StdIn for AutoIt
    # e.g. open a named pipe or file and write payload + newline
    print("[autoit_bridge] SEND:", payload)


def wait_for_ready(timeout=20):
    # TODO: implement your existing ready signal from AutoIt
    # For now, just sleep and assume ready
    start = time.time()
    while time.time() - start < timeout:
        time.sleep(0.5)
        return True
    return False


def mouse_delta(dx, dy):
    send_command("mouse_delta", {"dx": dx, "dy": dy})


def right_down():
    send_command("right_down", {})


def right_up():
    send_command("right_up", {})


def toggle_shiftlock():
    send_command("toggle_shiftlock", {})

def read_bot_state():
    return read_state()
