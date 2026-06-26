import threading
import time

from bot.bot_runtime import BotRuntime


class AIController:
    """
    Manages all AI bot runtimes.
    - start/stop bots
    - track running instances
    - expose state to UI
    """

    def __init__(self):
        self.bots = {}          # bot_name → BotRuntime
        self.threads = {}       # bot_name → Thread
        self.status = {}        # bot_name → status dict

    # ---------------------------------------------------------
    # Start a bot
    # ---------------------------------------------------------
    def start_bot(self, config: dict) -> bool:
        bot_name = config["bot_name"]

        if bot_name in self.bots:
            print(f"[AIController] Bot '{bot_name}' already running.")
            return False

        print(f"[AIController] Starting bot '{bot_name}'...")

        runtime = BotRuntime(config)
        self.bots[bot_name] = runtime

        t = threading.Thread(target=runtime.start, daemon=True)
        self.threads[bot_name] = t
        t.start()

        self.status[bot_name] = {
            "running": True,
            "last_update": time.time(),
            "username": config["bot_name"],
            "state": "starting"
        }

        return True

    # ---------------------------------------------------------
    # Stop a bot
    # ---------------------------------------------------------
    def stop_bot(self, bot_name: str) -> bool:
        if bot_name not in self.bots:
            print(f"[AIController] Bot '{bot_name}' not running.")
            return False

        print(f"[AIController] Stopping bot '{bot_name}'...")

        try:
            self.bots[bot_name].stop()
        except Exception as e:
            print("[AIController] Error stopping bot:", e)

        del self.bots[bot_name]
        del self.threads[bot_name]
        self.status[bot_name]["running"] = False
        self.status[bot_name]["state"] = "stopped"

        return True

    # ---------------------------------------------------------
    # Stop all bots
    # ---------------------------------------------------------
    def stop_all(self):
        print("[AIController] Stopping all bots...")
        for name in list(self.bots.keys()):
            self.stop_bot(name)

    # ---------------------------------------------------------
    # Get bot status for UI
    # ---------------------------------------------------------
    def get_status(self):
        out = {}
        for name, runtime in self.bots.items():
            try:
                state = runtime.brain.state
                out[name] = {
                    "running": True,
                    "yaw": state.camera.yaw,
                    "mode": state.behavior.mode,
                    "stuck": state.stuck,
                    "last_action": state.last_action_time,
                    "target": state.target.target_player,
                }
            except:
                out[name] = {"running": False}

        return out

    # ---------------------------------------------------------
    # Update loop for UI (optional)
    # ---------------------------------------------------------
    def tick(self):
        """
        Called by controller_main or controller_webui to refresh UI.
        """
        for name in list(self.bots.keys()):
            self.status[name]["last_update"] = time.time()
            self.status[name]["state"] = "running"
