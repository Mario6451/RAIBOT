import numpy as np
import cv2
import mss

class ScreenCapture:
    def __init__(self):
        self.sct = mss.mss()

    def grab(self):
        monitor = self.sct.monitors[1]
        img = np.array(self.sct.grab(monitor))
        img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
        return img
