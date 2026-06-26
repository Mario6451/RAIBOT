import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from settings import save_settings
from avatar_loader import load_avatar_ini, build_avatar_string, encode_avatar_binary


class SettingsUI:
    def __init__(self, root, settings):
        self.root = root
        self.settings = settings

        # Notebook (tabs)
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill="both", expand=True)

        # Create tabs
        self.general_tab = ttk.Frame(self.notebook)
        self.llm_tab = ttk.Frame(self.notebook)
        self.training_tab = ttk.Frame(self.notebook)
        self.performance_tab = ttk.Frame(self.notebook)
        self.avatar_tab = ttk.Frame(self.notebook)  # NEW TAB

        # Add tabs to notebook
        self.notebook.add(self.general_tab, text="General")
        self.notebook.add(self.llm_tab, text="LLM")
        self.notebook.add(self.training_tab, text="Training")
        self.notebook.add(self.performance_tab, text="Performance")
        self.notebook.add(self.avatar_tab, text="Avatar")  # NEW TAB

        # Build content inside each tab
        self._build_general_settings(self.general_tab)
        self._build_llm_settings(self.llm_tab)
        self._build_training_settings(self.training_tab)
        self._build_performance_settings(self.performance_tab)
        self._build_avatar_settings(self.avatar_tab)  # NEW TAB

        # Save button at bottom
        ttk.Button(root, text="Save All Settings", command=self._save_all).pack(pady=10)

    # ---------------------------------------------------------
    # GENERAL SETTINGS TAB
    # ---------------------------------------------------------
    def _build_general_settings(self, tab):
        frame = ttk.LabelFrame(tab, text="General Settings")
        frame.pack(fill="x", padx=10, pady=10)

        ttk.Label(frame, text="Bot Name:").pack(anchor="w")
        self.bot_name_var = tk.StringVar(value=self.settings["general"]["bot_name"])
        ttk.Entry(frame, textvariable=self.bot_name_var).pack(fill="x", pady=3)

        ttk.Label(frame, text="Model Name:").pack(anchor="w")
        self.model_var = tk.StringVar(value=self.settings["general"]["model"])
        ttk.Entry(frame, textvariable=self.model_var).pack(fill="x", pady=3)

        ttk.Label(frame, text="Model Endpoint:").pack(anchor="w")
        self.endpoint_var = tk.StringVar(value=self.settings["general"]["model_endpoint"])
        ttk.Entry(frame, textvariable=self.endpoint_var).pack(fill="x", pady=3)

        self.auto_launch_var = tk.BooleanVar(value=self.settings["general"]["auto_launch"])
        ttk.Checkbutton(frame, text="Auto-launch bot on start", variable=self.auto_launch_var).pack(anchor="w", pady=3)

        ttk.Label(frame, text="Default Bot EXE Path:").pack(anchor="w")
        self.exe_var = tk.StringVar(value=self.settings["general"]["default_exe_path"])
        ttk.Entry(frame, textvariable=self.exe_var).pack(fill="x", pady=3)

        ttk.Label(frame, text="Default Avatar File:").pack(anchor="w")
        self.avatar_var = tk.StringVar(value=self.settings["general"]["default_avatar"])
        ttk.Entry(frame, textvariable=self.avatar_var).pack(fill="x", pady=3)

    # ---------------------------------------------------------
    # LLM SETTINGS TAB
    # ---------------------------------------------------------
    def _build_llm_settings(self, tab):
        frame = ttk.LabelFrame(tab, text="LLM Settings")
        frame.pack(fill="x", padx=10, pady=10)

        ttk.Label(frame, text="Temperature:").pack(anchor="w")
        self.temp_var = tk.DoubleVar(value=self.settings["llm"]["temperature"])
        ttk.Entry(frame, textvariable=self.temp_var).pack(fill="x", pady=3)

        ttk.Label(frame, text="Max Tokens:").pack(anchor="w")
        self.tokens_var = tk.IntVar(value=self.settings["llm"]["max_tokens"])
        ttk.Entry(frame, textvariable=self.tokens_var).pack(fill="x", pady=3)

        ttk.Label(frame, text="System Prompt:").pack(anchor="w")
        self.prompt_text = tk.Text(frame, height=10, wrap="word")
        self.prompt_text.insert("1.0", self.settings["llm"]["system_prompt"])
        self.prompt_text.pack(fill="x", pady=3)

    # ---------------------------------------------------------
    # TRAINING SETTINGS TAB
    # ---------------------------------------------------------
    def _build_training_settings(self, tab):
        frame = ttk.LabelFrame(tab, text="AI Training Settings")
        frame.pack(fill="x", padx=10, pady=10)

        self.self_var = tk.BooleanVar(value=self.settings["training"]["self_learning"])
        ttk.Checkbutton(frame, text="Enable Self-Learning", variable=self.self_var).pack(anchor="w", pady=2)

        self.imitation_var = tk.BooleanVar(value=self.settings["training"]["imitation_learning"])
        ttk.Checkbutton(frame, text="Enable Imitation Learning", variable=self.imitation_var).pack(anchor="w", pady=2)

        self.instruction_var = tk.BooleanVar(value=self.settings["training"]["instruction_learning"])
        ttk.Checkbutton(frame, text="Enable Instruction Learning", variable=self.instruction_var).pack(anchor="w", pady=2)

    # ---------------------------------------------------------
    # PERFORMANCE SETTINGS TAB
    # ---------------------------------------------------------
    def _build_performance_settings(self, tab):
        frame = ttk.LabelFrame(tab, text="Performance Settings")
        frame.pack(fill="x", padx=10, pady=10)

        ttk.Label(frame, text="AI Tick Rate (Hz):").pack(anchor="w")
        self.tick_var = tk.IntVar(value=self.settings["performance"]["tick_rate"])
        ttk.Entry(frame, textvariable=self.tick_var).pack(fill="x", pady=3)

        ttk.Label(frame, text="Screen Capture FPS:").pack(anchor="w")
        self.capture_var = tk.IntVar(value=self.settings["performance"]["capture_fps"])
        ttk.Entry(frame, textvariable=self.capture_var).pack(fill="x", pady=3)

        ttk.Label(frame, text="Pathfinding Grid Size:").pack(anchor="w")
        self.grid_var = tk.IntVar(value=self.settings["performance"]["pathfinding_grid_size"])
        ttk.Entry(frame, textvariable=self.grid_var).pack(fill="x", pady=3)

        self.log_var = tk.BooleanVar(value=self.settings["performance"]["logging_enabled"])
        ttk.Checkbutton(frame, text="Enable Logging", variable=self.log_var).pack(anchor="w", pady=3)

    # ---------------------------------------------------------
    # AVATAR TAB (NEW)
    # ---------------------------------------------------------
    def _build_avatar_settings(self, tab):
        frame = ttk.LabelFrame(tab, text="Avatar Editor")
        frame.pack(fill="x", padx=10, pady=10)

        # Import button
        ttk.Button(frame, text="Import RBLXHUB avatar.ini", command=self._import_avatar_ini).pack(pady=5)

        # Editable fields
        self.avatar_fields = {}

        def add_field(label, key):
            ttk.Label(frame, text=label).pack(anchor="w")
            var = tk.StringVar()
            ttk.Entry(frame, textvariable=var).pack(fill="x", pady=2)
            self.avatar_fields[key] = var

        add_field("Name", "name")
        add_field("Player ID", "playerid")
        add_field("Membership", "membership")
        add_field("R15 (0=R6, 4=R15)", "r15")
        add_field("Body Colors (6)", "bodycolor")
        add_field("Hats (3)", "hats")
        add_field("Clothing (tshirt|shirt|pants)", "clothing")
        add_field("Face", "face")

        ttk.Button(frame, text="Rebuild Binary", command=self._rebuild_binary).pack(pady=5)

        ttk.Label(frame, text="Avatar Binary (UTF-16LE Hex):").pack(anchor="w")
        self.binary_box = tk.Text(frame, height=4)
        self.binary_box.pack(fill="x", pady=5)

    # ---------------------------------------------------------
    # IMPORT AVATAR.INI
    # ---------------------------------------------------------
    def _import_avatar_ini(self):
        path = filedialog.askopenfilename(
            title="Select RBLXHUB avatar.ini",
            filetypes=[("INI files", "*.ini")]
        )
        if not path:
            return

        try:
            data = load_avatar_ini(path)
            self.settings["avatar_data"] = data

            # Fill GUI fields
            self.avatar_fields["name"].set(data["name"])
            self.avatar_fields["playerid"].set(data["playerid"])
            self.avatar_fields["membership"].set(data["membership"])
            self.avatar_fields["r15"].set(data["r15"])
            self.avatar_fields["bodycolor"].set("|".join(str(x) for x in data["bodycolor"]))
            self.avatar_fields["hats"].set("|".join(str(x) for x in data["hats"]))
            self.avatar_fields["clothing"].set("|".join(str(x) for x in data["clothing"]))
            self.avatar_fields["face"].set(data["face"])

            # Build binary
            avatar_string = build_avatar_string(data)
            avatar_binary = encode_avatar_binary(avatar_string)
            self.settings["avatar_binary"] = avatar_binary

            self.binary_box.delete("1.0", tk.END)
            self.binary_box.insert(tk.END, avatar_binary)

            messagebox.showinfo("Success", "Avatar imported and converted.")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to import avatar.ini:\n{e}")

    # ---------------------------------------------------------
    # REBUILD BINARY FROM GUI FIELDS
    # ---------------------------------------------------------
    def _rebuild_binary(self):
        try:
            data = {
                "name": self.avatar_fields["name"].get(),
                "playerid": int(self.avatar_fields["playerid"].get()),
                "membership": self.avatar_fields["membership"].get(),
                "r15": int(self.avatar_fields["r15"].get()),
                "bodycolor": [int(x) for x in self.avatar_fields["bodycolor"].get().split("|")],
                "hats": [int(x) for x in self.avatar_fields["hats"].get().split("|")],
                "package": [0, 0, 0, 0, 0, 0],
                "clothing": [int(x) for x in self.avatar_fields["clothing"].get().split("|")],
                "face": int(self.avatar_fields["face"].get())
            }

            avatar_string = build_avatar_string(data)
            avatar_binary = encode_avatar_binary(avatar_string)

            self.settings["avatar_binary"] = avatar_binary
            self.settings["avatar_data"] = data

            self.binary_box.delete("1.0", tk.END)
            self.binary_box.insert(tk.END, avatar_binary)

            messagebox.showinfo("Success", "Avatar binary rebuilt.")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to rebuild binary:\n{e}")

    # ---------------------------------------------------------
    # SAVE ALL SETTINGS
    # ---------------------------------------------------------
    def _save_all(self):
        # General
        self.settings["general"]["bot_name"] = self.bot_name_var.get()
        self.settings["general"]["model"] = self.model_var.get()
        self.settings["general"]["model_endpoint"] = self.endpoint_var.get()
        self.settings["general"]["auto_launch"] = self.auto_launch_var.get()
        self.settings["general"]["default_exe_path"] = self.exe_var.get()
        self.settings["general"]["default_avatar"] = self.avatar_var.get()

        # LLM
        self.settings["llm"]["temperature"] = self.temp_var.get()
        self.settings["llm"]["max_tokens"] = self.tokens_var.get()
        self.settings["llm"]["system_prompt"] = self.prompt_text.get("1.0", "end").strip()

        # Training
        self.settings["training"]["self_learning"] = self.self_var.get()
        self.settings["training"]["imitation_learning"] = self.imitation_var.get()
        self.settings["training"]["instruction_learning"] = self.instruction_var.get()

        # Performance
        self.settings["performance"]["tick_rate"] = self.tick_var.get()
        self.settings["performance"]["capture_fps"] = self.capture_var.get()
        self.settings["performance"]["pathfinding_grid_size"] = self.grid_var.get()
        self.settings["performance"]["logging_enabled"] = self.log_var.get()

        # Avatar
        if "avatar_binary" in self.settings:
            self.settings["general"]["default_avatar"] = self.settings["avatar_binary"]

        save_settings(self.settings)
        print("[Settings] Saved successfully!")
