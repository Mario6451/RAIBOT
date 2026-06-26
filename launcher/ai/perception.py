import time
import re
import cv2
import numpy as np
from mss import mss
from typing import Optional, Dict, Any

from .state import AIState


class Perception:
    """
    Lightweight perception module:
    - movement detection
    - chat OCR
    - player detection (center-screen blob)
    - dynamic region scaling
    """

    def __init__(self):
        self.sct = mss()
        self.last_frame = None
        self.last_chat = ""
        self.last_capture = 0

        # Default 1280x720 regions (auto-scaled)
        self.regions = {
            "chat":  {"top": 600, "left": 20,  "width": 500, "height": 200},
            "center": {"top": 300, "left": 400, "width": 300, "height": 300},
            "full":  {"top": 0,   "left": 0,   "width": 1280, "height": 720}
        }

    # ---------------------------------------------------------
    # Region scaling for any Roblox window size
    # ---------------------------------------------------------
    def scale_regions(self, width: int, height: int):
        """Scale perception regions to match the actual Roblox window."""
        scale_x = width / 1280
        scale_y = height / 720

        for key, r in self.regions.items():
            r["top"] = int(r["top"] * scale_y)
            r["left"] = int(r["left"] * scale_x)
            r["width"] = int(r["width"] * scale_x)
            r["height"] = int(r["height"] * scale_y)

    # ---------------------------------------------------------
    # Main capture function
    # ---------------------------------------------------------
    def capture(self, state: AIState) -> Dict[str, Any]:
        now = time.time()
        if now - self.last_capture < 0.1:
            return {
                "chat_message": None,
                "chat_command": None,
                "player": None,
                "movement": False
            }

        self.last_capture = now

        frame = np.array(self.sct.grab(self.regions["full"]))[:, :, :3]

        movement = self._detect_movement(frame)
        chat_msg = self._detect_chat()
        chat_cmd = self._detect_chat_command(chat_msg)
        player = self._detect_player(frame)

        self.last_frame = frame
        state.mark_perception()

        return {
            "chat_message": chat_msg,
            "chat_command": chat_cmd,
            "player": player,
            "movement": movement
        }

    # ---------------------------------------------------------
    # Movement detection (frame differencing)
    # ---------------------------------------------------------
    def _detect_movement(self, frame) -> bool:
        if self.last_frame is None:
            return False

        diff = cv2.absdiff(frame, self.last_frame)
        gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
        score = np.sum(gray) / 255

        return score > 50000

    # ---------------------------------------------------------
    # Chat OCR
    # ---------------------------------------------------------
    def _detect_chat(self) -> Optional[str]:
        try:
            import pytesseract
        except:
            return None

        region = self.sct.grab(self.regions["chat"])
        img = np.array(region)[:, :, :3]

        text = pytesseract.image_to_string(img)
        lines = [l.strip() for l in text.split("\n") if l.strip()]

        if not lines:
            return None

        last = lines[-1]
        if last == self.last_chat:
            return None

        self.last_chat = last
        msg = re.sub(r"^\w+:\s*", "", last)
        return msg

    # ---------------------------------------------------------
    # Chat command detection
    # ---------------------------------------------------------
    def _detect_chat_command(self, msg: Optional[str]) -> Optional[str]:
        if not msg:
            return None

        lower = msg.lower()

        if "follow me" in lower:
            return "follow"
        if "stop" in lower:
            return "stop"
        if "come here" in lower:
            return "follow"
        if "wait" in lower:
            return "stop"

        return None

    # ---------------------------------------------------------
    # Player detection (simple blob in center region)
    # ---------------------------------------------------------
    def _detect_player(self, frame) -> Optional[Dict[str, Any]]:
        region = self.regions["center"]

        crop = frame[
            region["top"]:region["top"] + region["height"],
            region["left"]:region["left"] + region["width"]
        ]

        gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 80, 255, cv2.THRESH_BINARY_INV)

        contours, _ = cv2.findContours(
            thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )

        if not contours:
            return None

        cnt = max(contours, key=cv2.contourArea)
        area = cv2.contourArea(cnt)

        if area < 300:
            return None

        x, y, w, h = cv2.boundingRect(cnt)

        # Convert to pseudo-world coordinates
        world_x = (x - region["width"] / 2) / 10
        world_z = (y - region["height"] / 2) / 10
        distance = (world_x**2 + world_z**2) ** 0.5

        return {
            "pos": (world_x, 0, world_z),
            "distance": distance,
            "direction": np.arctan2(world_z, world_x)
        }
