import time
import threading
import json

from ai.brain import AIBrain
from ai.perception import Perception
from bot_loader import load_bot_profile
from bot_launcher import build_join_url, launch_client
from autoit_bridge import wait_for_ready
import server


class BotRuntime:
    """
    Main AI runtime loop.
    - loads profile
    - launches client
    - runs perception
    - runs AI brain
    - updates dashboard
    """

    def __init__(self, config):
        self.config = config
        self.running = False

        # Load bot profile
        self.profile = load_bot_profile(config["bot_name"])
        print(f"[Runtime] Loaded profile: {self.profile['Account']['username']}")

        # AI modules
        self.brain = AIBrain()
        self.perception = Perception()

    # ---------------------------------------------------------
    # Launch Roblox client
    # ---------------------------------------------------------
    def launch(self):
        client_path = self.config["client_path"]
        server_ip = self.config["server_ip"]
        server_port = self.config["server_port"]
        joinscript_path = self.config["joinscript_path"]

        join_url = build_join_url(
            base_url=joinscript_path,
            place_id=self.config["bot_attrs"].get("place_id", 0),
            ip=server_ip,
            port=server_port,
            user_id=self.profile["Account"]["user_id"],
            username=self.profile["Account"]["username"],
            membership=self.profile["Account"].get("membership", 0),
            binary="RobloxPlayerBeta.exe"
        )

        print(f"[Runtime] Join URL: {join_url}")
        launch_client(client_path, join_url)

        print("[Runtime] Waiting for AutoIt...")
        if not wait_for_ready(timeout=20):
            print("[Runtime] AutoIt did not signal ready. Aborting.")
            return False

        print("[Runtime] AutoIt ready.")
        return True

    # ---------------------------------------------------------
    # Main loop
    # ---------------------------------------------------------
    def start(self):
        if not self.launch():
            return

        self.running = True
        print(f"[Runtime] Bot '{self.profile['Account']['username']}' started.")

        tick_rate = 30
        tick_delay = 1.0 / tick_rate

        while self.running:
            try:
                # Capture perception
                world = self.perception.capture(self.brain.state)

                # Update AI brain
                self.brain.update(world)

                # Push state to Web UI
                server.update_bots([{
                    "name": self.profile["Account"]["username"],
                    "userId": self.profile["Account"]["user_id"],
                    "x": 0,
                    "y": 0,
                    "angle": self.brain.state.camera.yaw,
                    "status": "running"
                }])

            except Exception as e:
                print("[Runtime] Error:", e)

            time.sleep(tick_delay)

    # ---------------------------------------------------------
    # Stop bot
    # ---------------------------------------------------------
    def stop(self):
        self.running = False
        print(f"[Runtime] Bot '{self.profile['Account']['username']}' stopped.")


# Standalone mode for testing
if __name__ == "__main__":
    cfg = {
        "bot_name": "Bot 1",
        "client_path": "RobloxPlayerBeta.exe",
        "server_ip": "127.0.0.1",
        "server_port": 53640,
        "joinscript_path": None,
        "bot_attrs": {}
    }

    bot = BotRuntime(cfg)
    bot.start()
