import cv2
import numpy as np

def detect_player_color(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower = np.array([0, 50, 50])
    upper = np.array([10, 255, 255])
    mask = cv2.inRange(hsv, lower, upper)
    return mask

def detect_players(frame):
    mask = detect_player_color(frame)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    players = []
    for c in contours:
        area = cv2.contourArea(c)
        if area < 150:  
            continue

        x, y, w, h = cv2.boundingRect(c)
        cx = x + w // 2
        cy = y + h // 2

        players.append({
            "bbox": (x, y, w, h),
            "center": (cx, cy),
            "area": area
        })

    return players
