# launcher/controller/controller_processes.py

import psutil


class ProcessController:
    def __init__(self, main):
        self.main = main
        self.ui = main.ui

    def load_processes(self):
        items = []
        for p in psutil.process_iter(["pid", "name", "cpu_percent", "memory_info"]):
            try:
                pid = p.info["pid"]
                name = p.info["name"] or "unknown"
                cpu = p.info["cpu_percent"]
                mem = (p.info["memory_info"].rss / (1024 * 1024)) if p.info["memory_info"] else 0
                items.append(f"{pid:5d}  {name:30s}  CPU: {cpu:5.1f}%  RAM: {mem:6.1f} MB")
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

        self.ui.set_process_list(items)
