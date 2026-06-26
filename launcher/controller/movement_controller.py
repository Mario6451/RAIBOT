# controller/movement_controller.py

from controller.bridge_comm import BridgeComm

class MovementController:
    def __init__(self):
        self.bridge = BridgeComm()

    # Move to absolute world coordinate
    def move_to(self, x, z):
        self.bridge.mouse_abs(x, z, speed=0)
        self.bridge.right_down()
        self.bridge.right_up()

    # Move relative (for strafing, dodging)
    def move_delta(self, dx, dz):
        self.bridge.mouse_delta(dx, dz)

    # WASD movement
    def key_down(self, key):
        self.bridge.key_down(key)

    def key_up(self, key):
        self.bridge.key_up(key)

    def walk_forward(self):
        self.key_down("W")

    def stop_forward(self):
        self.key_up("W")

    def walk_backward(self):
        self.key_down("S")

    def stop_backward(self):
        self.key_up("S")

    def strafe_left(self):
        self.key_down("A")

    def stop_strafe_left(self):
        self.key_up("A")

    def strafe_right(self):
        self.key_down("D")

    def stop_strafe_right(self):
        self.key_up("D")

    def jump(self):
        self.key_down("SPACE")
        self.key_up("SPACE")

    # Attack-move
    def attack_move(self):
        self.bridge.attack_move()

    # Formation movement
    def formation_move(self, x, z):
        self.bridge.formation_move(x, z)
