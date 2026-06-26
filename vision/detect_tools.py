import cv2
import numpy as np

def detect_tools(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    yellow_low = np.array([20, 80, 80])
    yellow_high = np.array([35, 255, 255])
    mask_yellow = cv2.inRange(hsv, yellow_low, yellow_high)

    contours, _ = cv2.findContours(mask_yellow, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    tools = []
    for c in contours:
        area = cv2.contourArea(c)
        if area < 80:
            continue

        x, y, w, h = cv2.boundingRect(c)
        tools.append({
            "bbox": (x, y, w, h),
            "area": area
        })

    return tools
