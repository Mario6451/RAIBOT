import tkinter as tk
from tkinter import ttk


class PathDebugTab(ttk.Frame):
    """
    Pathfinding Debugger
    - shows open/closed nodes, last path, stuck points
    """

    def __init__(self, parent, controller_ai):
        super().__init__(parent)

        self.controller_ai = controller_ai
        self.selected_bot = tk.StringVar()

        self._build_ui()
        self._start_updater()

    def _build_ui(self):
        title = ttk.Label(self, text="Pathfinding Debugger", font=("Segoe UI", 14, "bold"))
        title.pack(pady=10)

        bot_frame = ttk.Frame(self)
        bot_frame.pack(pady=5)

        ttk.Label(bot_frame, text="Bot:").pack(side="left", padx=5)

        self.bot_dropdown = ttk.Combobox(
            bot_frame,
            textvariable=self.selected_bot,
            state="readonly",
            width=20
        )
        self.bot_dropdown.pack(side="left", padx=5)

        ttk.Button(bot_frame, text="Refresh", command=self._refresh_bot_list).pack(side="left", padx=5)

        # Text area
        self.text = tk.Text(self, wrap="none", bg="#1e1e1e", fg="#dcdcdc", height=20)
        self.text.pack(fill="both", expand=True, padx=10, pady=10)

    def _refresh_bot_list(self):
        bots = list(self.controller_ai.bots.keys())
        self.bot_dropdown["values"] = bots
        if bots:
            self.selected_bot.set(bots[0])

    def _start_updater(self):
        self.after(500, self._update)

    def _update(self):
        bot = self.selected_bot.get()
        rt = self.controller_ai.bots.get(bot)
        if not rt:
            self.text.delete("1.0", "end")
            self.text.insert("end", "No bot selected or bot not running.\n")
            self._start_updater()
            return

        s = rt.brain.state
        n = s.nav

        self.text.delete("1.0", "end")

        self.text.insert("end", f"Bot: {bot}\n\n")
        self.text.insert("end", f"Stuck: {s.stuck}\n")
        self.text.insert("end", f"Stuck Counter: {s.stuck_counter}\n")
        self.text.insert("end", f"Visited Points: {len(n.visited_points)}\n")
        self.text.insert("end", f"Stuck Points: {len(n.stuck_points)}\n")
        self.text.insert("end", f"Last Path Length: {len(n.last_path)}\n\n")

        self.text.insert("end", "Last Path:\n")
        for i, p in enumerate(n.last_path):
            self.text.insert("end", f"  {i}: {p}\n")

        self.text.insert("end", "\nVisited Points:\n")
        for i, p in enumerate(n.visited_points[:100]):
            self.text.insert("end", f"  {i}: {p}\n")

        self._start_updater()
