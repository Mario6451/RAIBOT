import subprocess
import time
import win32gui
import win32process
from PIL import ImageGrab

from core.avatar import load_avatar_ini
from core.sigma import make_sigma_binary
from core.joiner import build_join_url
from core.settings import SETTINGS

# Optional AI imports
ENABLE_AI = SETTINGS.get("enable_ai", True)
if ENABLE_AI:
    try:
        from ai import AI
        from movement import Movement
        from network import Network
        from state import BotState
        AI_AVAILABLE = True
    except:
        AI_AVAILABLE = False
else:
    AI_AVAILABLE = False

class RobloxClientController:
    def __init__(self, exe_path):
        self.exe_path = exe_path
        self.process = None
        self.hwnd = None
        self.running = False
        self.ai = None

    def launch(self, ip, port, username, user_id, membership, avatar_ini):
        avatar = load_avatar_ini(avatar_ini)
        sigma = make_sigma_binary(avatar)
        join_url = build_join_url(ip, port, username, user_id, membership, sigma)

        args = [
            self.exe_path,
            "-a", "http://www.rbolock.tk/",
            "-j", join_url,
            "-t", "1"
        ]

        self.process = subprocess.Popen(args)
        time.sleep(3)
        self.find_window()
        self.running = True

        if AI_AVAILABLE:
            self.ai = AI(username)
            self.ai.start()

    def find_window(self):
        def callback(hwnd, _):
            if win32gui.IsWindowVisible(hwnd):
                _, pid = win32process.GetWindowThreadProcessId(hwnd)
                if self.process and pid == self.process.pid:
                    self.hwnd = hwnd
        win32gui.EnumWindows(callback, None)

    def capture(self):
        if not self.hwnd:
            return None
        rect = win32gui.GetWindowRect(self.hwnd)
        return ImageGrab.grab(bbox=rect)

    def kill(self):
        if self.process:
            self.process.kill()
        if self.ai:
            self.ai.stop()
        self.running = False
