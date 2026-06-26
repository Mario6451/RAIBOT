# ai/vision.py

import cv2
import numpy as np
from mss import mss
import math


class Vision:
    """
    Unified vision module used by:
        - PerceptionModule
        - PlayerDetector (vision fallback)
        - MapScanner
    """

    def __init__(self):
        self.sct = mss()
        self.last_frame = None

    # ---------------------------------------------------------
    # SCREEN CAPTURE
    # ---------------------------------------------------------
    def capture_region(self, region):
        """
        region = {top, left, width, height}
        Returns BGR numpy array.
        """
        try:
            img = self.sct.grab(region)
            return np.array(img)[:, :, :3]
        except:
            return None

    # ---------------------------------------------------------
    # MOVEMENT DETECTION
    # ---------------------------------------------------------
    def detect_movement(self, frame):
        if frame is None:
            return False

        if self.last_frame is None:
            self.last_frame = frame
            return False

        diff = cv2.absdiff(frame, self.last_frame)
        gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
        score = np.sum(gray) / 255

        self.last_frame = frame
        return score > 50000

    # ---------------------------------------------------------
    # PLAYER CONTOUR DETECTION (fallback)
    # ---------------------------------------------------------
    def detect_player_contour(self, frame, region):
        """
        Vision fallback used by PlayerDetector.
        Detects a humanoid-like blob in the center region.
        """
        if frame is None:
            return None

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

        # Convert screen offset → approximate world offset
        world_x = (x - region["width"] / 2) / 10
        world_z = (y - region["height"] / 2) / 10
        distance = (world_x**2 + world_z**2) ** 0.5
        direction = math.atan2(world_z, world_x)

        return {
            "pos": (world_x, 0, world_z),
            "distance": distance,
            "direction": direction
        }
