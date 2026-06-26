# launcher/controller/controller_bots.py

import threading
import time
import subprocess
import os
import psutil
from tkinter import filedialog

from bot_runtime import run_bot
from dashboard import update_bots, update_map, add_log

# examples:
update_bots(bots_dict)
update_map(map_data)
add_log("Bot X did something")



class BotController:
    def __init__(self, main):
        self.main = main
        self.ui = main.ui

        self.running = False
        self.bots = [{"name": "Bot 1", "speed": 1.0, "aggression": 0.5}]
        self.current_bot = "Bot 1"

    # ---------------------------------------------------------
    # Start bot
    # ---------------------------------------------------------
    def start_bot(self):
        if self.running:
            self.ui.log_launcher("Bot already running.")
            return

        self._start_autoit_if_needed()

        self.running = True
        self.ui.update_status("Running")
        self.ui.log_launcher("Starting bot...")

        threading.Thread(target=self._run_bot_thread, daemon=True).start()
        threading.Thread(target=self._monitor_status, daemon=True).start()

    def _run_bot_thread(self):
        try:
            bot_name = self.current_bot
            client_path = self.ui.client_path_var.get().strip()
            server_ip = self.ui.server_ip_var.get().strip()
            server_port = int(self.ui.server_port_var.get().strip())
            joinscript_path = self.ui.joinscript_var.get().strip()

            bot_obj = next((b for b in self.bots if b["name"] == bot_name), None)

            config = {
                "bot_name": bot_name,
                "client_path": client_path,
                "server_ip": server_ip,
                "server_port": server_port,
                "joinscript_path": joinscript_path,
                "bot_attrs": bot_obj,
            }

            run_bot(config)

        except Exception as e:
            self.ui.log_launcher(f"Bot crashed: {e}")
            self.running = False
            self.ui.update_status("Crashed")

    # ---------------------------------------------------------
    # Stop / Restart
    # ---------------------------------------------------------
    def stop_bot(self):
        self.running = False
        self.ui.update_status("Stopped")
        self.ui.log_launcher("Bot stopped.")

    def restart_bot(self):
        self.stop_bot()
        time.sleep(0.5)
        self.start_bot()

    # ---------------------------------------------------------
    # Monitor bot + push to Web‑UI
    # ---------------------------------------------------------
    def _monitor_status(self):
        while self.running:
            self._check_autoit()

            # CPU + RAM
            p = psutil.Process()
            cpu = p.cpu_percent(interval=0.1)
            mem = p.memory_info().rss / (1024 * 1024)

            self.ui.update_cpu(cpu)
            self.ui.update_mem(mem)

            # Multi‑bot map
            bot_states = []
            map_states = []

            for bot in self.bots:
                bot_states.append({
                    "name": bot["name"],
                    "status": "running" if self.running else "stopped",
                    "speed": bot.get("speed", 1.0),
                    "aggression": bot.get("aggression", 0.5),
                })

                map_states.append({
                    "x": 250,
                    "y": 250,
                    "name": bot["name"]
                })

            # Update Tkinter map
            self.ui.update_map(
                [(250, 250, 45, bot["name"]) for bot in self.bots],
                [(150, 150)]
            )

            # Push to Web‑UI
            server.update_bots(bot_states)
            server.update_map(map_states)

            time.sleep(0.9)

    # ---------------------------------------------------------
    # AutoIt
    # ---------------------------------------------------------
    def _check_autoit(self):
        connected = os.path.exists("botcmd.txt")
        self.ui.update_autoit(connected)

    def _start_autoit_if_needed(self):
        for p in psutil.process_iter(["name"]):
            if "autoit" in (p.info["name"] or "").lower():
                return
        try:
            exe_path = os.path.abspath("autoit/bot.exe")
            subprocess.Popen([exe_path])
            self.ui.log_global(f"Started AutoIt bot: {exe_path}")
        except Exception as e:
            self.ui.log_global(f"Failed to start AutoIt bot: {e}")

    # ---------------------------------------------------------
    # Bot management
    # ---------------------------------------------------------
    def add_bot(self):
        new_name = f"Bot {len(self.bots) + 1}"
        self.bots.append({"name": new_name, "speed": 1.0, "aggression": 0.5})
        self.ui.bot_selector["values"] = [b["name"] for b in self.bots]
        self.ui.log_global(f"Added bot: {new_name}")

    def edit_current_bot(self):
        # (same as your original code)
        pass

    def on_bot_selected(self, event):
        idx = self.ui.bot_selector.current()
        if idx >= 0:
            self.current_bot = self.bots[idx]["name"]
            self.update_preview()

    def update_preview(self):
        self.ui.update_preview_text(f"Selected bot: {self.current_bot}")

    # ---------------------------------------------------------
    # File browsing
    # ---------------------------------------------------------
    def browse_client_path(self):
        path = filedialog.askopenfilename(
            title="Select Roblox Client",
            filetypes=[("Executable", "*.exe"), ("All files", "*.*")]
        )
        if path:
            self.ui.client_path_var.set(path)
            self.ui.log_global(f"Selected client: {path}")

    def browse_joinscript(self):
        path = filedialog.askopenfilename(
            title="Select JoinScript",
            filetypes=[("Lua", "*.lua"), ("All files", "*.*")]
        )
        if path:
            self.ui.joinscript_var.set(path)
            self.ui.log_global(f"Selected JoinScript: {path}")

    # ---------------------------------------------------------
    # Refresh
    # ---------------------------------------------------------
    def refresh_status(self):
        self._check_autoit()
        self.main.processes.load_processes()
        self.main.windows.refresh_windows()
        self.ui.log_launcher("Status refreshed.")
