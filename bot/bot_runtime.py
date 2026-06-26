import time
import os, sys

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from brain import AIBrain
from bot.bot_loader import load_bot_profile
from bot.bot_launcher import launch_client, build_join_url
from autoit_bridge import wait_for_ready
import server


def run_bot(config):
    bot_name = config["bot_name"]
    server_ip = config["server_ip"]
    server_port = config["server_port"]
    settings = config["settings"]

    launcher = settings["launcher"]
    client_path = launcher["client_path"]
    joinscript_url = launcher["joinscript_url"]
    place_id = int(launcher["place_id"])

    profile = load_bot_profile(bot_name)
    username = profile["Account"]["username"]
    user_id = profile["Account"]["user_id"]
    membership = profile["Account"].get("membership", 0)
    avatar_binary = profile["Account"]["avatar_binary"]

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

    launch_client(client_path, join_url)

    if not wait_for_ready(timeout=20):
        print("[Runtime] AutoIt did not signal ready.")
        return

    brain = AIBrain(
        bot_folder=f"bots/{bot_name}",
        settings=settings,
        debug_callback=lambda msg: print(f"[AI:{username}]", msg)
    )

    tick_rate = settings["performance"]["tick_rate"]
    tick_delay = 1.0 / tick_rate

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
