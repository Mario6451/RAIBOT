# ai/perception.py

import time, math, cv2, numpy as np
from mss import mss
from autoit_bridge import read_bot_state
from ai.chat_sniffer import ChatSniffer
from ai.player_detector import PlayerDetector
from ai.memory_reader_chat import MemoryChatReader
from ai.memory_reader_players import MemoryPlayerReader


class PerceptionModule:
    def __init__(self):
        self.sct = mss()
        self.last_frame = None
        self.last_capture = 0

        self.last_chat = ""
        self.chat_enabled = True

        self.last_player_pos = None
        self.player_enabled = True

        mon = self.sct.monitors[1]
        self.screen_w = mon["width"]
        self.screen_h = mon["height"]

        self.regions = {
            "chat":   {"top": 0.80, "left": 0.02, "width": 0.40, "height": 0.18},
            "center": {"top": 0.40, "left": 0.35, "width": 0.30, "height": 0.30},
            "full":   {"top": 0.00, "left": 0.00, "width": 1.00, "height": 1.00}
        }

        self.mem_chat = MemoryChatReader()
        self.mem_players = MemoryPlayerReader()

        self.chat_source = ChatSniffer(self.mem_chat, self)
        self.player_detector = PlayerDetector(self.mem_players, self)

    def _px(self, key):
        r = self.regions[key]
        return {
            "top":   int(r["top"]   * self.screen_h),
            "left":  int(r["left"]  * self.screen_w),
            "width": int(r["width"] * self.screen_w),
            "height":int(r["height"]* self.screen_h)
        }

    def capture(self):
        now = time.time()

        auto = read_bot_state()
        x = float(auto.get("x", 0))
        y = float(auto.get("y", 0))
        angle = float(auto.get("angle", 0))

        if now - self.last_capture < 0.10:
            return {
                "x": x, "y": y, "angle": angle,
                "chat_message": None,
                "chat_command": None,
                "player": self.last_player_pos,
                "movement": False
            }

        self.last_capture = now

        full = self._px("full")
        frame = np.array(self.sct.grab(full))[:, :, :3]

        movement = self._movement(frame)
        chat_msg = self.chat_source.get_latest_message()
        chat_cmd = self._chat_cmd(chat_msg)
        player = self.player_detector.get_nearest_player(frame)

        self.last_frame = frame
        self.last_player_pos = player

        return {
            "x": x, "y": y, "angle": angle,
            "chat_message": chat_msg,
            "chat_command": chat_cmd,
            "player": player,
            "movement": movement
        }

    def _movement(self, frame):
        if self.last_frame is None:
            return False
        diff = cv2.absdiff(frame, self.last_frame)
        gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
        return np.sum(gray) / 255 > 50000

    def read_chat(self):
        if not self.chat_enabled:
            return None
        try:
            import pytesseract
        except:
            return None

        region = self._px("chat")
        img = np.array(self.sct.grab(region))[:, :, :3]
        text = pytesseract.image_to_string(img)

        lines = [l.strip() for l in text.split("\n") if l.strip()]
        if not lines:
            return None

        last = lines[-1]
        if last == self.last_chat:
            return None

        self.last_chat = last
        return last

    def _chat_cmd(self, msg):
        if not msg:
            return None
        m = msg.lower()
        if "follow" in m: return "follow"
        if "stop" in m: return "stop"
        if "attack" in m: return "combat"
        return None

    def detect(self, frame):
        return self._vision(frame)

    def _vision(self, frame):
        if not self.player_enabled:
            return None

        region = self._px("center")
        crop = frame[
            region["top"]:region["top"] + region["height"],
            region["left"]:region["left"] + region["width"]
        ]

        gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 80, 255, cv2.THRESH_BINARY_INV)
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if not contours:
            return None

        cnt = max(contours, cv2.contourArea)
        if cv2.contourArea(cnt) < 300:
            return None

        x, y, w, h = cv2.boundingRect(cnt)
        world_x = (x - region["width"] / 2) / 10
        world_z = (y - region["height"] / 2) / 10

        return {
            "pos": (world_x, 0, world_z),
            "distance": (world_x**2 + world_z**2)**0.5,
            "direction": math.atan2(world_z, world_x)
        }
