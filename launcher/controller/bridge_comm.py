import requests
import socket
import json
import os


class BridgeComm:
    def __init__(self):
        self.http_url = "http://127.0.0.1:5005/command"
        self.tcp_host = "127.0.0.1"
        self.tcp_port = 5006
        self.cmd_file = "botcmd.txt"

    # -----------------------------
    # 1) HTTP
    # -----------------------------
    def send_http(self, data):
        try:
            r = requests.post(self.http_url, json=data, timeout=0.2)
            return r.status_code == 200
        except:
            return False

    # -----------------------------
    # 2) TCP
    # -----------------------------
    def send_tcp(self, data):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.2)
            s.connect((self.tcp_host, self.tcp_port))
            s.sendall(json.dumps(data).encode("utf-8"))
            s.close()
            return True
        except:
            return False

    # -----------------------------
    # 3) FILE FALLBACK
    # -----------------------------
    def send_file(self, data):
        try:
            with open(self.cmd_file, "w") as f:
                f.write(json.dumps(data))
            return True
        except:
            return False

    # -----------------------------
    # MASTER SEND FUNCTION
    # -----------------------------
    def send(self, data):
        if self.send_http(data):
            return "http"
        if self.send_tcp(data):
            return "tcp"
        self.send_file(data)
        return "file"

    # =========================================================
    # HIGH-LEVEL COMMAND HELPERS
    # =========================================================

    # -----------------------------
    # Mouse
    # -----------------------------
    def mouse_abs(self, x, y, speed=0):
        return self.send({"cmd": "mouse_abs", "x": x, "y": y, "speed": speed})

    def mouse_delta(self, dx, dy):
        return self.send({"cmd": "mouse_delta", "dx": dx, "dy": dy})

    def right_down(self):
        return self.send({"cmd": "right_down"})

    def right_up(self):
        return self.send({"cmd": "right_up"})

    def left_click(self):
        return self.send({"cmd": "left_click"})

    # -----------------------------
    # Keyboard
    # -----------------------------
    def key_down(self, key):
        return self.send({"cmd": "key_down", "key": key})

    def key_up(self, key):
        return self.send({"cmd": "key_up", "key": key})

    # -----------------------------
    # Sleep
    # -----------------------------
    def sleep(self, ms):
        return self.send({"cmd": "sleep", "ms": ms})

    # -----------------------------
    # Attack-Move
    # -----------------------------
    def attack_move(self):
        return self.send({"cmd": "attack_move"})

    # -----------------------------
    # Formation Movement
    # -----------------------------
    def formation_move(self, x, z):
        return self.send({"cmd": "formation_move", "x": x, "y": z})

    # -----------------------------
    # Camera Delta (yaw/pitch)
    # -----------------------------
    def camera_delta(self, dx, dy):
        return self.send({"cmd": "camera_delta", "dx": dx, "dy": dy})
