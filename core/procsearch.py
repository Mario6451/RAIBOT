import win32gui
import win32process
import win32api

def get_process_exe(pid):
    try:
        handle = win32api.OpenProcess(0x0400 | 0x0010, False, pid)
        exe = win32process.GetModuleFileNameEx(handle, 0)
        win32api.CloseHandle(handle)
        return exe
    except:
        return None

def list_processes():
    processes = []
    def callback(hwnd, _):
        if win32gui.IsWindowVisible(hwnd):
            try:
                _, pid = win32process.GetWindowThreadProcessId(hwnd)
                exe = get_process_exe(pid)
                if exe:
                    processes.append((pid, exe))
            except:
                pass
    win32gui.EnumWindows(callback, None)
    return processes

def search_processes(query):
    query = query.lower()
    return [(pid, exe) for pid, exe in list_processes() if query in exe.lower()]
