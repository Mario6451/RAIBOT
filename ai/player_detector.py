# ai/player_detector.py

import math


class PlayerDetector:
    def __init__(self, memory_reader=None, vision_detector=None):
        """
        memory_reader: object with .get_players() -> list of dicts
            Expected player dict format:
            {
                "pos": (x, y, z),
                "distance": float,
                "direction": float
            }

        vision_detector: object with ._detect_player_vision(frame) -> dict | None
        """
        self.memory_reader = memory_reader
        self.vision_detector = vision_detector

    # ---------------------------------------------------------
    # MAIN ENTRY: choose nearest player from memory or vision
    # ---------------------------------------------------------
    def get_nearest_player(self, frame=None):
        """
        Returns a unified player dict:
        {
            "pos": (x, y, z),
            "distance": float,
            "direction": float
        }
        """

        # -----------------------------
        # 1. MEMORY-BASED DETECTION
        # -----------------------------
        if self.memory_reader:
            try:
                players = self.memory_reader.get_players()
                if players:
                    # Ensure all players have distance
                    valid = [p for p in players if "distance" in p]
                    if valid:
                        return min(valid, key=lambda p: p["distance"])
            except Exception:
                pass

        # -----------------------------
        # 2. VISION-BASED DETECTION
        # -----------------------------
        if self.vision_detector and frame is not None:
            try:
                detected = self.vision_detector._detect_player_vision(frame)
                if detected:
                    return detected
            except Exception:
                return None

        # -----------------------------
        # 3. NOTHING FOUND
        # -----------------------------
        return None
