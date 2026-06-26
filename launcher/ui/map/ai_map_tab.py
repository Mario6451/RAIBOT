import tkinter as tk
from tkinter import ttk
import random
import math


class AIMapTab(ttk.Frame):
    """
    Ultra-Advanced Minimap:
    - Bot positions
    - Pathfinding lines
    - Hover tooltips
    - Unique color per bot
    - CLICK-TO-MOVE
    - ZOOM (mouse wheel)
    - PAN (right mouse drag)
    - MULTI-BOT SELECTION (shift-click + drag-select)
    - FORMATION MOVEMENT (line, wedge, circle)
    - ATTACK-MOVE
    - VISION CONES
    - HEATMAP OVERLAY
    - CAMERA TRACKING
    """

    def __init__(self, parent, controller_ai):
        super().__init__(parent)

        self.controller_ai = controller_ai
        self.bot_colors = {}
        self.hover_label = None

        # Map state
        self.map_size = 600
        self.scale = 4.0
        self.offset_x = 0
        self.offset_y = 0

        # Selection
        self.selected_bots = set()

        # Drag-select
        self.drag_start = None
        self.drag_rect = None

        # Pan
        self.pan_start = None

        # Heatmap
        self.heatmap = {}  # (x,z) → intensity

        # Camera tracking
        self.camera_follow = None

        self._build_ui()
        self._bind_events()
        self._start_updater()

    # ---------------------------------------------------------
    # UI Layout
    # ---------------------------------------------------------
    def _build_ui(self):
        title = ttk.Label(self, text="AI Minimap", font=("Segoe UI", 14, "bold"))
        title.pack(pady=10)

        # Formation buttons
        form_frame = ttk.Frame(self)
        form_frame.pack(pady=5)

        ttk.Button(form_frame, text="Line", command=lambda: self._formation("line")).pack(side="left", padx=5)
        ttk.Button(form_frame, text="Wedge", command=lambda: self._formation("wedge")).pack(side="left", padx=5)
        ttk.Button(form_frame, text="Circle", command=lambda: self._formation("circle")).pack(side="left", padx=5)
        ttk.Button(form_frame, text="Attack-Move", command=self._attack_move).pack(side="left", padx=5)

        # Canvas
        self.canvas = tk.Canvas(
            self,
            width=self.map_size,
            height=self.map_size,
            bg="#1e1e1e",
            highlightthickness=1,
            highlightbackground="#444"
        )
        self.canvas.pack(pady=10)

        self.hover_label = ttk.Label(self, text="", background="#333", foreground="white")
        self.hover_label.place_forget()

    # ---------------------------------------------------------
    # Event Bindings
    # ---------------------------------------------------------
    def _bind_events(self):
        self.canvas.bind("<Motion>", self._on_mouse_move)

        # Click-to-move + selection
        self.canvas.bind("<Button-1>", self._on_left_click)

        # Drag-select
        self.canvas.bind("<ButtonPress-1>", self._on_drag_start)
        self.canvas.bind("<B1-Motion>", self._on_drag_move)
        self.canvas.bind("<ButtonRelease-1>", self._on_drag_end)

        # Pan
        self.canvas.bind("<Button-3>", self._on_right_click)
        self.canvas.bind("<B3-Motion>", self._on_pan_drag)

        # Zoom
        self.canvas.bind("<MouseWheel>", self._on_zoom)

    # ---------------------------------------------------------
    # Bot color assignment
    # ---------------------------------------------------------
    def _get_bot_color(self, bot_name):
        if bot_name not in self.bot_colors:
            r = random.randint(100, 255)
            g = random.randint(100, 255)
            b = random.randint(100, 255)
            self.bot_colors[bot_name] = f"#{r:02x}{g:02x}{b:02x}"
        return self.bot_colors[bot_name]

    # ---------------------------------------------------------
    # Coordinate transforms
    # ---------------------------------------------------------
    def _world_to_canvas(self, x, z):
        cx = self.map_size / 2 + (x * self.scale) + self.offset_x
        cz = self.map_size / 2 + (z * self.scale) + self.offset_y
        return cx, cz

    def _canvas_to_world(self, cx, cz):
        x = (cx - self.map_size / 2 - self.offset_x) / self.scale
        z = (cz - self.map_size / 2 - self.offset_y) / self.scale
        return x, z

    # ---------------------------------------------------------
    # Drawing
    # ---------------------------------------------------------
    def _draw_map(self):
        self.canvas.delete("all")

        # HEATMAP
        for (x, z), intensity in self.heatmap.items():
            cx, cz = self._world_to_canvas(x, z)
            color = f"#{intensity:02x}0000"
            self.canvas.create_oval(cx-3, cz-3, cx+3, cz+3, fill=color, outline="")

        status = self.controller_ai.get_status()

        for bot_name, data in status.items():
            if not data.get("running"):
                continue

            x = data.get("x", 0)
            z = data.get("y", 0)

            cx, cz = self._world_to_canvas(x, z)
            color = self._get_bot_color(bot_name)

            # Vision cone
            yaw = data.get("yaw", 0)
            self._draw_vision_cone(cx, cz, yaw, color)

            # Bot dot
            r = 6
            outline = "white" if bot_name in self.selected_bots else ""
            width = 2 if bot_name in self.selected_bots else 1

            self.canvas.create_oval(
                cx - r, cz - r, cx + r, cz + r,
                fill=color,
                outline=outline,
                width=width,
                tags=("bot", bot_name)
            )

            # Name
            self.canvas.create_text(cx, cz + 12, text=bot_name, fill=color, font=("Segoe UI", 8))

            # Path
            path = data.get("path", [])
            if len(path) > 1:
                for i in range(len(path) - 1):
                    x1, z1 = path[i]
                    x2, z2 = path[i + 1]
                    c1 = self._world_to_canvas(x1, z1)
                    c2 = self._world_to_canvas(x2, z2)
                    self.canvas.create_line(c1[0], c1[1], c2[0], c2[1], fill=color, width=2)

            # Camera follow
            if self.camera_follow == bot_name:
                self.offset_x = self.map_size/2 - cx
                self.offset_y = self.map_size/2 - cz

    # ---------------------------------------------------------
    # Vision cone
    # ---------------------------------------------------------
    def _draw_vision_cone(self, cx, cz, yaw, color):
        length = 40 * self.scale
        angle = math.radians(yaw)

        x2 = cx + math.cos(angle) * length
        y2 = cz + math.sin(angle) * length

        self.canvas.create_line(cx, cz, x2, y2, fill=color, width=1, dash=(3, 3))

    # ---------------------------------------------------------
    # Hover tooltip
    # ---------------------------------------------------------
    def _on_mouse_move(self, event):
        x, y = event.x, event.y

        items = self.canvas.find_overlapping(x - 2, y - 2, x + 2, y + 2)
        for item in items:
            tags = self.canvas.gettags(item)
            if "bot" in tags:
                bot_name = tags[1]
                self.hover_label.config(text=bot_name)
                self.hover_label.place(x=x + 15, y=y + 15)
                return

        self.hover_label.place_forget()

    # ---------------------------------------------------------
    # CLICK-TO-MOVE + SHIFT MULTI-SELECT
    # ---------------------------------------------------------
    def _on_left_click(self, event):
        # Shift-click = toggle selection
        if event.state & 0x0001:
            self._shift_select(event)
            return

        # Normal click = move selected bots
        world_x, world_z = self._canvas_to_world(event.x, event.y)

        # Heatmap update
        self.heatmap[(int(world_x), int(world_z))] = min(255, self.heatmap.get((int(world_x), int(world_z)), 0) + 40)

        for bot in self.selected_bots:
            rt = self.controller_ai.bots.get(bot)
            if rt:
                rt.brain.command_move_to(world_x, world_z)

    def _shift_select(self, event):
        items = self.canvas.find_overlapping(event.x - 3, event.y - 3, event.x + 3, event.y + 3)
        for item in items:
            tags = self.canvas.gettags(item)
            if "bot" in tags:
                bot_name = tags[1]
                if bot_name in self.selected_bots:
                    self.selected_bots.remove(bot_name)
                else:
                    self.selected_bots.add(bot_name)

    # ---------------------------------------------------------
    # DRAG-SELECT
    # ---------------------------------------------------------
    def _on_drag_start(self, event):
        self.drag_start = (event.x, event.y)

    def _on_drag_move(self, event):
        if not self.drag_start:
            return

        x1, y1 = self.drag_start
        x2, y2 = event.x, event.y

        if self.drag_rect:
            self.canvas.delete(self.drag_rect)

        self.drag_rect = self.canvas.create_rectangle(
            x1, y1, x2, y2,
            outline="cyan",
            dash=(3, 3)
        )

    def _on_drag_end(self, event):
        if not self.drag_start:
            return

        x1, y1 = self.drag_start
        x2, y2 = event.x, event.y

        self.drag_start = None

        if self.drag_rect:
            self.canvas.delete(self.drag_rect)
            self.drag_rect = None

        # Select bots inside rectangle
        self.selected_bots.clear()

        items = self.canvas.find_enclosed(x1, y1, x2, y2)
        for item in items:
            tags = self.canvas.gettags(item)
            if "bot" in tags:
                self.selected_bots.add(tags[1])

    # ---------------------------------------------------------
    # FORMATION MOVEMENT
    # ---------------------------------------------------------
    def _formation(self, mode):
        if not self.selected_bots:
            return

        # Center of selected bots
        xs = []
        zs = []
        for bot in self.selected_bots:
            s = self.controller_ai.get_status().get(bot, {})
            xs.append(s.get("x", 0))
            zs.append(s.get("y", 0))

        cx = sum(xs) / len(xs)
        cz = sum(zs) / len(zs)

        # Formation offsets
        offsets = []

        if mode == "line":
            spacing = 6
            for i in range(len(self.selected_bots)):
                offsets.append((i * spacing, 0))

        elif mode == "wedge":
            spacing = 6
            for i in range(len(self.selected_bots)):
                offsets.append((i * spacing, (i % 2) * spacing))

        elif mode == "circle":
            radius = 10
            for i in range(len(self.selected_bots)):
                angle = (i / len(self.selected_bots)) * math.tau
                offsets.append((math.cos(angle) * radius, math.sin(angle) * radius))

        # Apply formation
        for (bot, (ox, oz)) in zip(self.selected_bots, offsets):
            rt = self.controller_ai.bots.get(bot)
            if rt:
                rt.brain.command_move_to(cx + ox, cz + oz)

    # ---------------------------------------------------------
    # ATTACK-MOVE
    # ---------------------------------------------------------
    def _attack_move(self):
        for bot in self.selected_bots:
            rt = self.controller_ai.bots.get(bot)
            if rt:
                rt.brain.state.behavior.mode = "attack_move"

    # ---------------------------------------------------------
    # PAN (right mouse drag)
    # ---------------------------------------------------------
    def _on_right_click(self, event):
        self.pan_start = (event.x, event.y)

    def _on_pan_drag(self, event):
        dx = event.x - self.pan_start[0]
        dy = event.y - self.pan_start[1]

        self.offset_x += dx
        self.offset_y += dy

        self.pan_start = (event.x, event.y)

    # ---------------------------------------------------------
    # ZOOM (mouse wheel)
    # ---------------------------------------------------------
    def _on_zoom(self, event):
        if event.delta > 0:
            self.scale *= 1.1
        else:
            self.scale /= 1.1

        self.scale = max(1.0, min(self.scale, 40.0))

    # ---------------------------------------------------------
    # Auto-refresh
    # ---------------------------------------------------------
    def _start_updater(self):
        self._draw_map()
        self.after(100, self._start_updater)
