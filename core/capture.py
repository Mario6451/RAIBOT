from PIL import ImageGrab
import win32gui

def capture_window(hwnd):
    if not hwnd:
        return None
    rect = win32gui.GetWindowRect(hwnd)
    return ImageGrab.grab(bbox=rect)
