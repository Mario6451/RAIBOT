import os
import time
import json

CMD_FILE = "botcmd.txt"
STATE_FILE = "botstate.txt"


def send_command(cmd_type, data=None):
    """
    Sends a command to AutoIt by writing JSON into botcmd.txt.
    AutoIt reads it, executes it, then clears the file.
    """
    payload = {
        "type": cmd_type,
        "data": data or {}
    }

    with open(CMD_FILE, "w", encoding="utf-8") as f:
        f.write(json.dumps(payload))

    return True


def read_bot_state():
    """
    Reads botstate.txt written by AutoIt.
    Expected format:
    {
        "x": float,
        "y": float,
        "angle": float,
        "ready": bool
    }
    """
    if not os.path.exists(STATE_FILE):
        return None

    try:
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            raw = f.read().strip()
            if not raw:
                return None
            return json.loads(raw)
    except:
        return None


def wait_for_ready(timeout=10):
    """
    Waits for AutoIt to signal readiness by writing:
    {"ready": true}
    """
    start = time.time()

    while time.time() - start < timeout:
        state = read_bot_state()
        if state and state.get("ready"):
            return True
        time.sleep(0.1)

    return False
