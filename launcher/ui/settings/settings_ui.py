import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext
from settings import load_settings, save_settings

import subprocess
import webbrowser
import threading


class SettingsUI:
    def __init__(self, root, settings):
        self.root = root
        self.settings = settings

        self.root.title("RAI Settings")
        self.root.geometry("650x650")
        self.root.configure(bg="#ECE9D8")  # XP-style background

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True)

        # Tabs
        self.general_tab = ttk.Frame(self.notebook)
        self.llm_tab = ttk.Frame(self.notebook)
        self.performance_tab = ttk.Frame(self.notebook)
        self.training_tab = ttk.Frame(self.notebook)

        self.notebook.add(self.general_tab, text="General")
        self.notebook.add(self.llm_tab, text="LLM")
        self.notebook.add(self.performance_tab, text="Performance")
        self.notebook.add(self.training_tab, text="Training")

        # Build UI
        self._build_general_settings(self.general_tab)
        self._build_llm_settings(self.llm_tab)
        self._build_performance_settings(self.performance_tab)
        self._build_training_settings(self.training_tab)

        # Save button
        ttk.Button(self.root, text="Save Settings", command=self._save).pack(pady=10)

    # ---------------------------------------------------------
    # GENERAL TAB
    # ---------------------------------------------------------
    def _build_general_settings(self, frame):
        general = self.settings["general"]
        row = 0

        ttk.Label(frame, text="Bot Name:").grid(row=row, column=0, sticky="w", pady=5)
        self.bot_name_var = tk.StringVar(value=general.get("bot_name", "RAI Bot"))
        ttk.Entry(frame, textvariable=self.bot_name_var).grid(row=row, column=1, sticky="ew")
        row += 1

        ttk.Label(frame, text="Client Path:").grid(row=row, column=0, sticky="w", pady=5)
        self.client_path_var = tk.StringVar(value=general.get("client_path", ""))
        ttk.Entry(frame, textvariable=self.client_path_var).grid(row=row, column=1, sticky="ew")
        ttk.Button(frame, text="Browse", command=self._browse_client).grid(row=row, column=2, padx=5)
        row += 1

        ttk.Label(frame, text="Default EXE Path:").grid(row=row, column=0, sticky="w", pady=5)
        self.default_exe_var = tk.StringVar(value=general.get("default_exe_path", ""))
        ttk.Entry(frame, textvariable=self.default_exe_var).grid(row=row, column=1, sticky="ew")
        ttk.Button(frame, text="Browse", command=self._browse_exe).grid(row=row, column=2, padx=5)
        row += 1

        ttk.Label(frame, text="Default Avatar:").grid(row=row, column=0, sticky="w", pady=5)
        self.default_avatar_var = tk.StringVar(value=general.get("default_avatar", ""))
        ttk.Entry(frame, textvariable=self.default_avatar_var).grid(row=row, column=1, sticky="ew")
        ttk.Button(frame, text="Browse", command=self._browse_avatar).grid(row=row, column=2, padx=5)
        row += 1

        ttk.Label(frame, text="Default JoinScript URL:").grid(row=row, column=0, sticky="w", pady=5)
        self.default_joinscript_var = tk.StringVar(value=general.get("default_joinscript_url", ""))
        ttk.Entry(frame, textvariable=self.default_joinscript_var).grid(row=row, column=1, sticky="ew")
        row += 1

        ttk.Label(frame, text="RCCService IP:").grid(row=row, column=0, sticky="w", pady=5)
        self.rcc_ip_var = tk.StringVar(value=general.get("rcc_ip", "127.0.0.1"))
        ttk.Entry(frame, textvariable=self.rcc_ip_var).grid(row=row, column=1, sticky="ew")
        row += 1

        ttk.Label(frame, text="RCCService Port:").grid(row=row, column=0, sticky="w", pady=5)
        self.rcc_port_var = tk.StringVar(value=str(general.get("rcc_port", 64989)))
        ttk.Entry(frame, textvariable=self.rcc_port_var).grid(row=row, column=1, sticky="ew")
        row += 1

        ttk.Label(frame, text="Model:").grid(row=row, column=0, sticky="w", pady=5)
        self.model_var = tk.StringVar(value=general.get("model", "microsoft/phi-4-mini-reasoning"))
        ttk.Entry(frame, textvariable=self.model_var).grid(row=row, column=1, sticky="ew")
        row += 1

        ttk.Label(frame, text="Model Endpoint:").grid(row=row, column=0, sticky="w", pady=5)
        self.model_endpoint_var = tk.StringVar(value=general.get("model_endpoint", "http://localhost:1234/v1/chat/completions"))
        ttk.Entry(frame, textvariable=self.model_endpoint_var).grid(row=row, column=1, sticky="ew")
        row += 1

        self.auto_launch_var = tk.BooleanVar(value=general.get("auto_launch", False))
        ttk.Checkbutton(frame, text="Auto-launch client", variable=self.auto_launch_var).grid(row=row, column=0, sticky="w", pady=5)
        row += 1

        # Start Web UI + Start Bot buttons
        ttk.Button(frame, text="Start Web UI", command=self._start_web_ui).grid(row=row, column=0, pady=10, sticky="w")
        ttk.Button(frame, text="Start Bot", command=self._start_bot).grid(row=row, column=1, pady=10, sticky="w")
        row += 1

        frame.columnconfigure(1, weight=1)

    # ---------------------------------------------------------
    # FILE PICKERS
    # ---------------------------------------------------------
    def _browse_client(self):
        path = filedialog.askopenfilename(title="Select Roblox Client")
        if path:
            self.client_path_var.set(path)

    def _browse_exe(self):
        path = filedialog.askopenfilename(title="Select EXE")
        if path:
            self.default_exe_var.set(path)

    def _browse_avatar(self):
        path = filedialog.askopenfilename(title="Select Avatar Image")
        if path:
            self.default_avatar_var.set(path)

    # ---------------------------------------------------------
    # START WEB UI
    # ---------------------------------------------------------
    def _start_web_ui(self):
        def run_server():
            try:
                subprocess.Popen(["python", "dashboard/server.py"])
            except Exception as e:
                print("[UI] Failed to start Web UI:", e)

        threading.Thread(target=run_server, daemon=True).start()
        webbrowser.open("http://127.0.0.1:5000")

    # ---------------------------------------------------------
    # START BOT
    # ---------------------------------------------------------
    def _start_bot(self):
        try:
            subprocess.Popen(["python", "bot/bot_runtime.py"])
        except Exception as e:
            print("[UI] Failed to start bot:", e)

    # ---------------------------------------------------------
    # LLM TAB
    # ---------------------------------------------------------
    def _build_llm_settings(self, frame):
        llm = self.settings["llm"]
        row = 0

        ttk.Label(frame, text="Temperature:").grid(row=row, column=0, sticky="w", pady=5)
        self.temperature_var = tk.StringVar(value=str(llm.get("temperature", 0.8)))
        ttk.Entry(frame, textvariable=self.temperature_var).grid(row=row, column=1, sticky="ew")
        row += 1

        ttk.Label(frame, text="Max Tokens:").grid(row=row, column=0, sticky="w", pady=5)
        self.max_tokens_var = tk.StringVar(value=str(llm.get("max_tokens", 4096)))
        ttk.Entry(frame, textvariable=self.max_tokens_var).grid(row=row, column=1, sticky="ew")
        row += 1

        ttk.Label(frame, text="System Prompt:").grid(row=row, column=0, sticky="nw", pady=5)
        self.system_prompt_box = scrolledtext.ScrolledText(frame, width=50, height=15)
        self.system_prompt_box.insert("1.0", llm.get("system_prompt", ""))
        self.system_prompt_box.grid(row=row, column=1, sticky="ew")
        row += 1

        frame.columnconfigure(1, weight=1)

    # ---------------------------------------------------------
    # PERFORMANCE TAB
    # ---------------------------------------------------------
    def _build_performance_settings(self, frame):
        perf = self.settings["performance"]
        row = 0

        ttk.Label(frame, text="Tick Rate:").grid(row=row, column=0, sticky="w", pady=5)
        self.tick_rate_var = tk.StringVar(value=str(perf.get("tick_rate", 30)))
        ttk.Entry(frame, textvariable=self.tick_rate_var).grid(row=row, column=1, sticky="ew")
        row += 1

        ttk.Label(frame, text="Capture FPS:").grid(row=row, column=0, sticky="w", pady=5)
        self.capture_fps_var = tk.StringVar(value=str(perf.get("capture_fps", 12)))
        ttk.Entry(frame, textvariable=self.capture_fps_var).grid(row=row, column=1, sticky="ew")
        row += 1

        ttk.Label(frame, text="Pathfinding Grid Size:").grid(row=row, column=0, sticky="w", pady=5)
        self.grid_size_var = tk.StringVar(value=str(perf.get("pathfinding_grid_size", 64)))
        ttk.Entry(frame, textvariable=self.grid_size_var).grid(row=row, column=1, sticky="ew")
        row += 1

        self.logging_enabled_var = tk.BooleanVar(value=perf.get("logging_enabled", True))
        ttk.Checkbutton(frame, text="Enable Logging", variable=self.logging_enabled_var).grid(row=row, column=0, sticky="w", pady=5)

        frame.columnconfigure(1, weight=1)

    # ---------------------------------------------------------
    # TRAINING TAB
    # ---------------------------------------------------------
    def _build_training_settings(self, frame):
        train = self.settings["training"]

        self.self_learning_var = tk.BooleanVar(value=train.get("self_learning", True))
        ttk.Checkbutton(frame, text="Self Learning", variable=self.self_learning_var).pack(anchor="w", pady=5)

        self.imitation_learning_var = tk.BooleanVar(value=train.get("imitation_learning", True))
        ttk.Checkbutton(frame, text="Imitation Learning", variable=self.imitation_learning_var).pack(anchor="w", pady=5)

        self.instruction_learning_var = tk.BooleanVar(value=train.get("instruction_learning", True))
        ttk.Checkbutton(frame, text="Instruction Learning", variable=self.instruction_learning_var).pack(anchor="w", pady=5)

    # ---------------------------------------------------------
    # SAVE
    # ---------------------------------------------------------
    def _save(self):
        self.settings["general"]["bot_name"] = self.bot_name_var.get()
        self.settings["general"]["client_path"] = self.client_path_var.get()
        self.settings["general"]["auto_launch"] = self.auto_launch_var.get()
        self.settings["general"]["default_exe_path"] = self.default_exe_var.get()
        self.settings["general"]["default_avatar"] = self.default_avatar_var.get()
        self.settings["general"]["default_joinscript_url"] = self.default_joinscript_var.get()
        self.settings["general"]["rcc_ip"] = self.rcc_ip_var.get()
        self.settings["general"]["rcc_port"] = int(self.rcc_port_var.get())
        self.settings["general"]["model"] = self.model_var.get()
        self.settings["general"]["model_endpoint"] = self.model_endpoint_var.get()

        self.settings["llm"]["temperature"] = float(self.temperature_var.get())
        self.settings["llm"]["max_tokens"] = int(self.max_tokens_var.get())
        self.settings["llm"]["system_prompt"] = self.system_prompt_box.get("1.0", "end").strip()

        self.settings["performance"]["tick_rate"] = int(self.tick_rate_var.get())
        self.settings["performance"]["capture_fps"] = int(self.capture_fps_var.get())
        self.settings["performance"]["pathfinding_grid_size"] = int(self.grid_size_var.get())
        self.settings["performance"]["logging_enabled"] = self.logging_enabled_var.get()

        self.settings["training"]["self_learning"] = self.self_learning_var.get()
        self.settings["training"]["imitation_learning"] = self.imitation_learning_var.get()
        self.settings["training"]["instruction_learning"] = self.instruction_learning_var.get()

        save_settings(self.settings)
