import tkinter as tk
from tkinter import ttk


class AILogsTab(ttk.Frame):
    """
    AI Logs Tab
    - live log viewer
    - filters by category
    """

    def __init__(self, parent, controller_ai):
        super().__init__(parent)

        self.controller_ai = controller_ai
        self.filter_var = tk.StringVar(value="all")

        self._build_ui()
        self._start_updater()

    def _build_ui(self):
        title = ttk.Label(self, text="AI Logs", font=("Segoe UI", 14, "bold"))
        title.pack(pady=10)

        filter_frame = ttk.Frame(self)
        filter_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(filter_frame, text="Filter:").pack(side="left", padx=5)

        filters = ["all", "movement", "perception", "pathfinding", "behavior", "error"]
        self.filter_dropdown = ttk.Combobox(
            filter_frame,
            textvariable=self.filter_var,
            values=filters,
            state="readonly",
            width=15
        )
        self.filter_dropdown.pack(side="left", padx=5)

        # Log text
        text_frame = ttk.Frame(self)
        text_frame.pack(fill="both", expand=True, padx=10, pady=5)

        self.text = tk.Text(text_frame, wrap="none", bg="#1e1e1e", fg="#dcdcdc")
        self.text.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(text_frame, orient="vertical", command=self.text.yview)
        scrollbar.pack(side="right", fill="y")
        self.text.configure(yscrollcommand=scrollbar.set)

    def _start_updater(self):
        self.after(500, self._update_logs)

    def _update_logs(self):
        # Expect controller_ai to have a log buffer per bot or global
        logs = getattr(self.controller_ai, "logs", [])
        filt = self.filter_var.get()

        self.text.delete("1.0", "end")
        for entry in logs[-500:]:
            category = entry.get("category", "all")
            if filt != "all" and category != filt:
                continue
            line = f"[{entry.get('time','')}] [{category}] {entry.get('bot','?')}: {entry.get('message','')}\n"
            self.text.insert("end", line)

        self._start_updater()
