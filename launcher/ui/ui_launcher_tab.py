# launcher/ui/ui_launcher_tab.py

import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext


class LauncherTab(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        self.controller = controller
        self._build_ui()

    # ---------------------------------------------------------
    # UI BUILD
    # ---------------------------------------------------------
    def _build_ui(self):
        # Left panel
        left = ttk.Frame(self)
        left.pack(side="left", fill="y", padx=10, pady=10)

        # Bot selector
        ttk.Label(left, text="Bot:").pack(anchor="w")
        self.bot_selector = ttk.Combobox(left, state="readonly")
        self.bot_selector.pack(fill="x")
        self.bot_selector.bind("<<ComboboxSelected>>", self.controller.on_bot_selected)

        # Start / Stop / Restart
        ttk.Button(left, text="▶ Start Bot", command=self.controller.start_bot).pack(fill="x", pady=2)
        ttk.Button(left, text="⏹ Stop Bot", command=self.controller.stop_bot).pack(fill="x", pady=2)
        ttk.Button(left, text="🔄 Restart Bot", command=self.controller.restart_bot).pack(fill="x", pady=2)

        ttk.Separator(left).pack(fill="x", pady=10)

        # Client path
        ttk.Label(left, text="Roblox Client:").pack(anchor="w")
        self.client_path_var = tk.StringVar()
        ttk.Entry(left, textvariable=self.client_path_var).pack(fill="x")
        ttk.Button(left, text="Browse", command=self.controller.browse_client_path).pack(fill="x", pady=2)

        # JoinScript
        ttk.Label(left, text="JoinScript:").pack(anchor="w")
        self.joinscript_var = tk.StringVar()
        ttk.Entry(left, textvariable=self.joinscript_var).pack(fill="x")
        ttk.Button(left, text="Browse", command=self.controller.browse_joinscript).pack(fill="x", pady=2)

        ttk.Separator(left).pack(fill="x", pady=10)

        # Server IP / Port
        ttk.Label(left, text="Server IP:").pack(anchor="w")
        self.server_ip_var = tk.StringVar()
        ttk.Entry(left, textvariable=self.server_ip_var).pack(fill="x")

        ttk.Label(left, text="Server Port:").pack(anchor="w")
        self.server_port_var = tk.StringVar()
        ttk.Entry(left, textvariable=self.server_port_var).pack(fill="x")

        ttk.Separator(left).pack(fill="x", pady=10)

        # Web‑UI
        ttk.Label(left, text="Web‑UI:").pack(anchor="w")
        ttk.Button(left, text="🌐 Open Dashboard", command=self.controller.open_dashboard).pack(fill="x", pady=2)
        ttk.Button(left, text="🔄 Restart Web‑UI", command=self.controller.restart_server).pack(fill="x", pady=2)
        ttk.Button(left, text="📁 Logs Folder", command=self.controller.open_logs).pack(fill="x", pady=2)

        ttk.Separator(left).pack(fill="x", pady=10)

        # Status
        ttk.Label(left, text="Status:").pack(anchor="w")
        self.status_var = tk.StringVar(value="Idle")
        ttk.Label(left, textvariable=self.status_var).pack(anchor="w")

        ttk.Label(left, text="CPU:").pack(anchor="w")
        self.cpu_var = tk.StringVar(value="0%")
        ttk.Label(left, textvariable=self.cpu_var).pack(anchor="w")

        ttk.Label(left, text="RAM:").pack(anchor="w")
        self.mem_var = tk.StringVar(value="0 MB")
        ttk.Label(left, textvariable=self.mem_var).pack(anchor="w")

        ttk.Label(left, text="AutoIt:").pack(anchor="w")
        self.autoit_var = tk.StringVar(value="Disconnected")
        ttk.Label(left, textvariable=self.autoit_var).pack(anchor="w")

        # ---------------------------------------------------------
        # RIGHT SIDE — MAP + LOGS
        # ---------------------------------------------------------
        right = ttk.Frame(self)
        right.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        # Map preview
        ttk.Label(right, text="Map Preview:").pack(anchor="w")
        self.map_canvas = tk.Canvas(right, width=300, height=300, bg="#1e1e1e")
        self.map_canvas.pack(pady=5)

        # Logs
        ttk.Label(right, text="Launcher Log:").pack(anchor="w")
        self.log_box = scrolledtext.ScrolledText(right, height=12, state="disabled")
        self.log_box.pack(fill="both", expand=True)

    # ---------------------------------------------------------
    # UI UPDATE METHODS
    # ---------------------------------------------------------
    def update_status(self, text):
        self.status_var.set(text)

    def update_cpu(self, value):
        self.cpu_var.set(f"{value:.1f}%")

    def update_mem(self, value):
        self.mem_var.set(f"{value:.1f} MB")

    def update_autoit(self, connected):
        self.autoit_var.set("Connected" if connected else "Disconnected")

    def update_map(self, bot_positions, player_positions):
        self.map_canvas.delete("all")

        # Draw bots
        for x, y, angle, name in bot_positions:
            self.map_canvas.create_oval(x-5, y-5, x+5, y+5, fill="cyan")
            self.map_canvas.create_text(x, y-10, text=name, fill="white")

        # Draw players
        for x, y in player_positions:
            self.map_canvas.create_oval(x-5, y-5, x+5, y+5, fill="yellow")

    def update_preview_text(self, text):
        self.log_launcher(text)

    def log_launcher(self, msg):
        self.log_box.configure(state="normal")
        self.log_box.insert("end", msg + "\n")
        self.log_box.configure(state="disabled")
        self.log_box.see("end")

    def log_global(self, msg):
        self.log_launcher("[GLOBAL] " + msg)
