import tkinter as tk
from tkinter import ttk, filedialog


def build_launcher_tab(ui):
    frame = ui.launcher_tab

    title = ttk.Label(frame, text="🤖 Roblox AI Player", font=("Segoe UI", 20, "bold"))
    title.pack(pady=10)

    status_frame = ttk.Frame(frame)
    status_frame.pack(pady=10)

    ui.status_label = ttk.Label(status_frame, text="Status: Idle", font=("Segoe UI", 11))
    ui.status_label.grid(row=0, column=0, padx=10)

    ui.autoit_label = ttk.Label(status_frame, text="AutoIt: ❌", font=("Segoe UI", 11))
    ui.autoit_label.grid(row=0, column=1, padx=10)

    ui.fps_label = ttk.Label(status_frame, text="Tick Rate: --", font=("Segoe UI", 11))
    ui.fps_label.grid(row=0, column=2, padx=10)

    ui.cpu_label = ttk.Label(status_frame, text="CPU: --%", font=("Segoe UI", 11))
    ui.cpu_label.grid(row=1, column=0, padx=10)

    ui.mem_label = ttk.Label(status_frame, text="RAM: -- MB", font=("Segoe UI", 11))
    ui.mem_label.grid(row=1, column=1, padx=10)

    bot_frame = ttk.Frame(frame)
    bot_frame.pack(pady=5)

    ttk.Label(bot_frame, text="Bot:", font=("Segoe UI", 10)).grid(row=0, column=0, padx=5)
    ui.bot_selector = ttk.Combobox(bot_frame, values=["Bot 1"], state="readonly", width=20)
    ui.bot_selector.current(0)
    ui.bot_selector.grid(row=0, column=1, padx=5)

    ui.add_bot_btn = ttk.Button(bot_frame, text="➕ Add Bot")
    ui.add_bot_btn.grid(row=0, column=2, padx=5)

    ui.edit_bot_btn = ttk.Button(bot_frame, text="✏️ Edit Bot")
    ui.edit_bot_btn.grid(row=0, column=3, padx=5)

    ttk.Label(bot_frame, text="Client EXE:", font=("Segoe UI", 10)).grid(row=1, column=0, padx=5)
    ui.client_path_var = tk.StringVar(value=ui.load_setting("client_path", ""))
    ui.client_path_entry = ttk.Entry(bot_frame, textvariable=ui.client_path_var, width=40)
    ui.client_path_entry.grid(row=1, column=1, padx=5)

    def browse_client():
        path = filedialog.askopenfilename(
            title="Select Roblox Client Executable",
            filetypes=[("Executable", "*.exe")]
        )
        if path:
            ui.client_path_var.set(path)
            ui.save_setting("client_path", path)

    ui.client_browse_btn = ttk.Button(bot_frame, text="📂 Browse", command=browse_client)
    ui.client_browse_btn.grid(row=1, column=2, padx=5)

    ttk.Label(bot_frame, text="JoinScript URL:", font=("Segoe UI", 10)).grid(row=2, column=0, padx=5)
    ui.joinscript_var = tk.StringVar(
        value=ui.load_setting("joinscript_url", "https://www.rbolock.tk/game/join2017.php")
    )
    ui.joinscript_entry = ttk.Entry(bot_frame, textvariable=ui.joinscript_var, width=40)
    ui.joinscript_entry.grid(row=2, column=1, padx=5)

    def save_joinscript_url(*_):
        ui.save_setting("joinscript_url", ui.joinscript_var.get())

    ui.joinscript_var.trace_add("write", save_joinscript_url)

    server_frame = ttk.Frame(frame)
    server_frame.pack(pady=5)

    ttk.Label(server_frame, text="Server IP:", font=("Segoe UI", 10)).grid(row=0, column=0, padx=5)
    ui.server_ip_var = tk.StringVar(value="127.0.0.1")
    ui.server_ip_entry = ttk.Entry(server_frame, textvariable=ui.server_ip_var, width=15)
    ui.server_ip_entry.grid(row=0, column=1, padx=5)

    ttk.Label(server_frame, text="Port:", font=("Segoe UI", 10)).grid(row=0, column=2, padx=5)
    ui.server_port_var = tk.StringVar(value="5000")
    ui.server_port_entry = ttk.Entry(server_frame, textvariable=ui.server_port_var, width=6)
    ui.server_port_entry.grid(row=0, column=3, padx=5)

    ttk.Label(server_frame, text="Place ID:", font=("Segoe UI", 10)).grid(row=1, column=0, padx=5)
    ui.place_id_var = tk.StringVar(value=ui.load_setting("place_id", "0"))
    ui.place_id_entry = ttk.Entry(server_frame, textvariable=ui.place_id_var, width=15)
    ui.place_id_entry.grid(row=1, column=1, padx=5)

    def save_place_id(*_):
        ui.save_setting("place_id", ui.place_id_var.get())

    ui.place_id_var.trace_add("write", save_place_id)

    btn_frame = ttk.Frame(frame)
    btn_frame.pack(pady=10)

    ui.start_btn = ttk.Button(btn_frame, text="▶️ Start", command=ui.start_bot)
    ui.start_btn.grid(row=0, column=0, padx=10)

    ui.stop_btn = ttk.Button(btn_frame, text="⏹️ Stop", command=ui.stop_bot)
    ui.stop_btn.grid(row=0, column=1, padx=10)

    ui.restart_btn = ttk.Button(btn_frame, text="🔁 Restart", command=ui.restart_bot)
    ui.restart_btn.grid(row=0, column=2, padx=10)

    ui.refresh_btn = ttk.Button(btn_frame, text="🔄 Refresh", command=ui.refresh_bots)
    ui.refresh_btn.grid(row=0, column=3, padx=10)

    extra_btn_frame = ttk.Frame(frame)
    extra_btn_frame.pack(pady=5)

    ui.open_dashboard_btn = ttk.Button(extra_btn_frame, text="📊 Web‑UI", command=ui.open_dashboard)
    ui.open_dashboard_btn.grid(row=0, column=0, padx=10)

    ui.open_logs_btn = ttk.Button(extra_btn_frame, text="📁 Logs Folder", command=ui.open_logs_folder)
    ui.open_logs_btn.grid(row=0, column=1, padx=10)

    ui.launcher_log = tk.Text(frame, height=8, width=130, state="disabled")
    ui.launcher_log.pack(pady=10)

    def log_launcher(text):
        ui.launcher_log.config(state="normal")
        ui.launcher_log.insert("end", text + "\n")
        ui.launcher_log.see("end")
        ui.launcher_log.config(state="disabled")

    ui.log_launcher = log_launcher

    def update_status(text):
        ui.status_label.config(text=f"Status: {text}")

    def update_autoit(connected: bool):
        ui.autoit_label.config(text=f"AutoIt: {'✅' if connected else '❌'}")

    def update_cpu(val):
        ui.cpu_label.config(text=f"CPU: {val:.1f}%")

    def update_mem(val):
        ui.mem_label.config(text=f"RAM: {val:.1f} MB")

    ui.update_status = update_status
    ui.update_autoit = update_autoit
    ui.update_cpu = update_cpu
    ui.update_mem = update_mem
