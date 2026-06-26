# movement.py

from autoit_bridge import (
    cam_left, cam_right, cam_up, cam_down,
    cam_zoom_in, cam_zoom_out, cam_reset,
    mouse_delta,
    right_down_cmd, right_up_cmd,
)

import mouse_look


class MovementController:
    def __init__(self, stats: dict | None = None):
        self.stats = stats or {}
        self.state = None

    # --- keyboard camera ---

    def camera_left(self): cam_left()
    def camera_right(self): cam_right()
    def camera_up(self): cam_up()
    def camera_down(self): cam_down()
    def camera_zoom_in(self): cam_zoom_in()
    def camera_zoom_out(self): cam_zoom_out()
    def camera_reset(self): cam_reset()

    # --- smooth mouse-look ---

    def look_smooth(self, dx: int, dy: int):
        mouse_look.look(dx, dy, smooth=True)

    def look_raw(self, dx: int, dy: int):
        mouse_look.look(dx, dy, smooth=False)

    # --- AutoIt-based mouse delta ---

    def look_autoit(self, dx: int, dy: int):
        right_down_cmd()
        mouse_delta(dx, dy)
        right_up_cmd()

    # --- first-person toggle ---

    def toggle_first_person(self):
        mouse_look.toggle_first_person()
