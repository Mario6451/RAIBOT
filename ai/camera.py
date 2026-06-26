import random

class CameraModule:
    def __init__(self, controller):
        self.controller = controller

    def wiggle(self):
        if random.random() < 0.6:
            self.controller._camera_wiggle()
