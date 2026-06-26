# launcher/controller/controller_webui.py

import subprocess
import threading
import webbrowser
import psutil
import os
from dashboard import start_server

# wherever you start the dashboard:
start_server(ip="127.0.0.1", port=5000)



class WebUIController:
    def __init__(self, main):
        self.main = main
        self.ui = main.ui

    # ---------------------------------------------------------
    # Start server
    # ---------------------------------------------------------
    def start_server(self):
        cfg = self.main.settings.settings["web_ui"]
        if not cfg["enabled"]:
            return

        threading.Thread(
            target=lambda: server.start_server(cfg["ip"], cfg["port"]),
            daemon=True
        ).start()

    # ---------------------------------------------------------
    # Restart server
    # ---------------------------------------------------------
    def restart_server(self):
        # Kill existing server
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
        url = f"http://{cfg['ip']}:{cfg['port']}"
        webbrowser.open(url)
        self.ui.log_launcher(f"Opened Web‑UI at {url}")

    # ---------------------------------------------------------
    # Logs folder
    # ---------------------------------------------------------
    def open_logs(self):
        os.makedirs("logs", exist_ok=True)
        subprocess.Popen(["explorer", os.path.abspath("logs")])
