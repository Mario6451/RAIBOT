# launcher/controller/controller_webui.py

import subprocess
import threading
import webbrowser
import psutil
import os
from dashboard.server import start_server   # FIXED IMPORT


class WebUIController:
    def __init__(self, main):
        self.main = main
        self.ui = main.ui

    # ---------------------------------------------------------
    # Start server
    # ---------------------------------------------------------
    def start_server(self):
        cfg = self.main.settings.settings["web_ui"]
        if not cfg.get("enabled", True):
            return

        ip = cfg.get("ip", "127.0.0.1")
        port = cfg.get("port", 5000)

        threading.Thread(
            target=lambda: start_server(ip, port),
            daemon=True
        ).start()

        self.ui.log_global(f"🌐 Web‑UI server started at http://{ip}:{port}")

    # ---------------------------------------------------------
    # Restart server
    # ---------------------------------------------------------
    def restart_server(self):
        # Kill existing server processes
        for p in psutil.process_iter(["cmdline"]):
            cmd = p.info["cmdline"] or []
            if "server.py" in " ".join(cmd):
                try:
                    p.terminate()
                except:
                    pass

        # Restart
        self.start_server()
        self.ui.log_global("🔄 Web‑UI server restarted.")

    # ---------------------------------------------------------
    # Open dashboard
    # ---------------------------------------------------------
    def open_dashboard(self):
        cfg = self.main.settings.settings["web_ui"]
        ip = cfg.get("ip", "127.0.0.1")
        port = cfg.get("port", 5000)

        url = f"http://{ip}:{port}"
        webbrowser.open(url)
        self.ui.log_launcher(f"Opened Web‑UI at {url}")

    # ---------------------------------------------------------
    # Logs folder
    # ---------------------------------------------------------
    def open_logs(self):
        os.makedirs("logs", exist_ok=True)
        subprocess.Popen(["explorer", os.path.abspath("logs")])
