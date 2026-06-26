# launcher/controller/controller_windows.py

import ctypes
from ctypes import wintypes
import psutil


class WindowController:
    def __init__(self, main):
        self.main = main
        self.ui = main.ui

        self.user32 = ctypes.WinDLL("user32", use_last_error=True)
        self.EnumWindows = self.user32.EnumWindows
        self.EnumWindowsProc = ctypes.WINFUNCTYPE(ctypes.c_bool, wintypes.HWND, wintypes.LPARAM)
        self.IsWindowVisible = self.user32.IsWindowVisible
        self.GetWindowTextW = self.user32.GetWindowTextW
        self.GetWindowTextLengthW = self.user32.GetWindowTextLengthW
        self.GetWindowThreadProcessId = self.user32.GetWindowThreadProcessId
        self.ShowWindow = self.user32.ShowWindow
        self.SetForegroundWindow = self.user32.SetForegroundWindow
        self.PostMessageW = self.user32.PostMessageW

        self.SW_MINIMIZE = 6
        self.SW_RESTORE = 9
        self.WM_CLOSE = 0x0010

    # ---------------------------------------------------------
    # Window enumeration
    # ---------------------------------------------------------
    def refresh_windows(self):
        windows = []

        def callback(hwnd, lParam):
            if not self.IsWindowVisible(hwnd):
                return True

            length = self.GetWindowTextLengthW(hwnd)
            if length == 0:
                return True

            title = ctypes.create_unicode_buffer(length + 1)
            self.GetWindowTextW(hwnd, title, length + 1)

            pid = wintypes.DWORD()
            self.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))

            try:
                p = psutil.Process(pid.value)
                pname = p.name()
            except:
                pname = "unknown"

            windows.append({
                "handle": hwnd,
                "title": title.value,
                "pid": pid.value,
                "process_name": pname,
                "tag": ""
            })

            return True

        self.EnumWindows(self.EnumWindowsProc(callback), 0)
        self.ui.set_window_list(windows)

    # ---------------------------------------------------------
    # Window actions
    # ---------------------------------------------------------
    def focus_window(self, h):
        self.SetForegroundWindow(h)

    def minimize_window(self, h):
        self.ShowWindow(h, self.SW_MINIMIZE)

    def close_window(self, h):
        self.PostMessageW(h, self.WM_CLOSE, 0, 0)
