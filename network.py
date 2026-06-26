import time
import os
import random

from state import WorldState
from dashboard.server import update_bot_state, bot_registry

class RobloxBotClient:
    def __init__(self, username, userid, membership, ip, port,
                 avatar, ai, movement_controller_cls, bot_folder):

        self.username = username
        self.userid = userid
        self.membership = membership

        # Game server
        self.ip = ip
        self.port = port

        # Avatar data
        self.avatar = avatar

        # AI + movement
        self.ai = ai
        self.state = WorldState()
        self.movement = movement_controller_cls(self)

        # Connection state
        self.connected = False
        self.bot_folder = bot_folder

        # Human-like tick timing
        self.base_tick = 0.20
        self.tick_variance = 0.12

        # Multi-bot coordination memory
        self.last_action = "idle"
        self.intent = None

    # ---------------------------------------------------------
    # Connection
    # ---------------------------------------------------------
    def connect(self):
        print(f"[Network] Connecting bot:")
        print(f"  Username: {self.username}")
        print(f"  UserId:   {self.userid}")
        print(f"  Member:   {self.membership}")
        print(f"  Game IP:  {self.ip}")
        print(f"  Port:     {self.port}")

        # In a real revival, this would handshake with the client.
        self.connected = True

    # ---------------------------------------------------------
    # Fake recv loop (placeholder for real revival)
    # ---------------------------------------------------------
    def recv_loop_once(self):
        # Simulate player position updates
        self.state.update_self(
            self.state.self_pos["x"] + random.uniform(-0.1, 0.1),
            3.0,
            self.state.self_pos["z"] + random.uniform(-0.1, 0.1)
        )

        # Simulate another player nearby
        self.state.update_player(
            self.username + "_friend",
            5.0 + random.uniform(-1, 1),
            3.0,
            2.0 + random.uniform(-1, 1)
        )

    # ---------------------------------------------------------
    # Dashboard control (manual override)
    # ---------------------------------------------------------
    def handle_dashboard_control(self, s):
        control = bot_registry.get(self.username, {}).get("control")
        if not control:
            return False

        act = control.get("action")

        if act == "wander":
            self.movement.wander(s)
            return True

        if act == "idle":
            self.movement.idle()
            return True

        if act == "follow":
            target = control.get("target", self.username)
            self.movement.follow_player(target, s)
            return True

        if act == "move_to":
            x = control.get("x", 0)
            z = control.get("z", 0)
            self.movement.move_to(x, z)
            return True

        if act == "emote":
            kind = control.get("type", "wave")
            self.movement.emote(kind)
            return True

        return False

    # ---------------------------------------------------------
    # AI tick (human-like timing + intent prediction)
    # ---------------------------------------------------------
    def tick_ai(self):
        s = self.state.to_dict()

        # Read last chat
        chat_path = os.path.join(self.bot_folder, "lastchat.txt")
        memory_path = os.path.join(self.bot_folder, "chatmemory.txt")

        last_chat = ""
        if os.path.exists(chat_path):
            with open(chat_path, "r", encoding="utf-8") as f:
                last_chat = f.read().strip()
            open(chat_path, "w").close()

        # If chat addressed to bot, store in memory
        if last_chat.lower().startswith(self.username.lower()):
            with open(memory_path, "a", encoding="utf-8") as mem:
                mem.write(last_chat + "\n")
            user_command = last_chat[len(self.username):].strip()
        else:
            user_command = ""

        # Dashboard override
        if self.handle_dashboard_control(s):
            action = {"action": "dashboard_control"}

        else:
            # AI decides action
            action = self.ai.decide(s, user_command)

            # Intent prediction (human-like)
            self.intent = action["action"]

            # Execute action
            if action["action"] == "follow":
                self.movement.follow_player(action["target"], s)

            elif action["action"] == "move_to":
                self.movement.move_to(action["x"], action["z"])

            elif action["action"] == "say":
                self.movement.say(action["text"])

            elif action["action"] == "use":
                self.movement.use_item(action["item"])

            elif action["action"] == "wander":
                self.movement.wander(s)

            elif action["action"] == "idle":
                self.movement.idle()

            elif action["action"] == "emote":
                self.movement.emote(action.get("type", "wave"))

        self.last_action = action["action"]

        # Dashboard update
        update_bot_state(self.username, {
            "name": self.username,
            "position": (
                self.state.self_pos["x"],
                self.state.self_pos["y"],
                self.state.self_pos["z"]
            ),
            "mood": self.ai.mood,
            "personality": self.ai.personality,
            "last_chat": last_chat,
            "action": action["action"],
            "intent": self.intent,
            "map": getattr(self.movement.scanner, "grid", None)
        })

    # ---------------------------------------------------------
    # Main loop (human-like tick timing)
    # ---------------------------------------------------------
    def run(self):
        self.connect()
        if not self.connected:
            print("[Network] Not connected.")
            return

        print("[Network] Bot loop starting.")

        try:
            while True:
                # Simulate receiving world updates
                self.recv_loop_once()

                # AI + movement tick
                self.tick_ai()

                # Human-like tick timing
                delay = self.base_tick + random.uniform(-self.tick_variance, self.tick_variance)
                delay = max(0.05, delay)
                time.sleep(delay)

        except KeyboardInterrupt:
            print("[Network] Bot stopped.")
