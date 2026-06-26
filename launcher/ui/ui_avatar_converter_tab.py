import tkinter as tk
from tkinter import ttk, filedialog

class AvatarConverterTab(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        ttk.Label(self, text="Avatar Converter", font=("Segoe UI", 12, "bold")).pack(anchor="w", pady=5)

        ttk.Label(self, text="Select RBLXHUB avatar.ini:").pack(anchor="w")
        self.avatar_path_var = tk.StringVar()
        ttk.Entry(self, textvariable=self.avatar_path_var).pack(fill="x")
        ttk.Button(self, text="Browse", command=self.browse_avatar).pack(pady=3)

        ttk.Label(self, text="Target Version:").pack(anchor="w", pady=(10, 0))
        self.version_var = tk.StringVar()
        self.version_dropdown = ttk.Combobox(self, textvariable=self.version_var, state="readonly")
        self.version_dropdown.pack(fill="x")

        ttk.Button(self, text="Convert", command=self.controller.convert_avatar).pack(pady=10)

        ttk.Label(self, text="Preview:").pack(anchor="w")
        self.preview_box = tk.Text(self, height=12)
        self.preview_box.pack(fill="both", expand=True)

        ttk.Button(self, text="Save to Bot", command=self.controller.save_converted_avatar).pack(pady=5)

    def browse_avatar(self):
        path = filedialog.askopenfilename(title="Select avatar.ini", filetypes=[("INI Files", "*.ini")])
        if path:
            self.avatar_path_var.set(path)

    def show_preview(self, text):
        self.preview_box.delete("1.0", tk.END)
        self.preview_box.insert(tk.END, text)
