# bot_runtime.py

import time

from bot_loader import load_bot_profile
from bot_launcher import build_join_url, launch_client
from ai.brain import AIBrain
from autoit_bridge import wait_for_ready
import server


def run_bot(config):
    """
    config = {
        "bot_name": str,
        "server_ip": str,
        "server_port": int,
        "settings": {
            "launcher": {
                "client_path": str,
                "joinscript_url": str,
                "place_id": str
            },
            "performance": {...},
            "movement": {...},
            "training": {...}
        }
    }
    """

    bot_name = config["bot_name"]
    server_ip = config["server_ip"]
    server_port = config["server_port"]
    settings = config["settings"]

    launcher = settings["launcher"]
    client_path = launcher["client_path"]
    joinscript_url = launcher["joinscript_url"]
    place_id = int(launcher["place_id"])

    # ---------------------------------------------------------
    # LOAD BOT PROFILE
    # ---------------------------------------------------------
    profile = load_bot_profile(bot_name)
    username = profile["Account"]["username"]
    user_id = profile["Account"]["user_id"]
    membership = profile["Account"].get("membership", 0)
    avatar_binary = profile["Account"]["avatar_binary"]

    print(f"[Runtime] Loaded profile: {username} ({user_id})")

    # ---------------------------------------------------------
    # BUILD JOIN URL
    # ---------------------------------------------------------
    join_url = build_join_url(
        base_url=joinscript_url,
        place_id=place_id,
        ip=server_ip,
        port=server_port,
        user_id=user_id,
        username=username,
        membership=membership,
        avatar_binary=avatar_binary
    )

    print(f"[Runtime] Join URL: {join_url}")

    # ---------------------------------------------------------
    # LAUNCH CLIENT
    # ---------------------------------------------------------
    launch_client(client_path, join_url)

    # ---------------------------------------------------------
    # WAIT FOR AUTOIT
    # ---------------------------------------------------------
    print("[Runtime] Waiting for AutoIt...")
    if not wait_for_ready(timeout=20):
        print("[Runtime] AutoIt did not signal ready. Aborting.")
        return

    print("[Runtime] AutoIt ready.")

    # ---------------------------------------------------------
    # START AI BRAIN
    # ---------------------------------------------------------
    brain = AIBrain(
        bot_folder=f"bots/{bot_name}",
        settings=settings,
        debug_callback=lambda msg: print(f"[AI:{username}]", msg)
    )

    tick_rate = settings["performance"]["tick_rate"]
    tick_delay = 1.0 / tick_rate

    print(f"[Runtime] Bot '{username}' started with tick rate {tick_rate} TPS.")

    # ---------------------------------------------------------
    # MAIN LOOP
    # ---------------------------------------------------------
    while True:
        try:
            brain.update()

            server.update_bots([{
                "name": username,
                "userId": user_id,
                "x": brain.state.x,
                "y": brain.state.y,
                "angle": brain.state.angle,
                "status": "running"
            }])

        except Exception as e:
            print("[Runtime] Error:", e)

        time.sleep(tick_delay)
