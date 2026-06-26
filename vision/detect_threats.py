import cv2
import numpy as np

def detect_threats(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    danger_low = np.array([0, 120, 120])
    danger_high = np.array([10, 255, 255])
    mask = cv2.inRange(hsv, danger_low, danger_high)

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    threats = []
    for c in contours:
        area = cv2.contourArea(c)
        if area < 120:
            continue

        x, y, w, h = cv2.boundingRect(c)
        threats.append({
            "bbox": (x, y, w, h),
            "area": area
        })

    return threats
