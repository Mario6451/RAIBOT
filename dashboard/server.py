# dashboard/server.py — FULL UPGRADED VERSION WITH LEGACY SUPPORT + BOT START/STOP

from flask import Flask, jsonify, request, render_template
from flask_socketio import SocketIO
import threading
import time
import json
import os

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="threading")

# ---------------------------------------------------------
# GLOBAL STATE (thread-safe)
# ---------------------------------------------------------
STATE = {
    "bots": {},            # {bot_name: {...state...}}
    "map": [],             # list of {x, y, name}
    "logs": [],            # global logs
    "personality": {},     # persona data
    "settings": {},        # settings.json flattened
}

STATE_LOCK = threading.Lock()

SAVE_DIR = "dashboard"
SAVE_PATH = os.path.join(SAVE_DIR, "state.json")

# ---------------------------------------------------------
# LOAD / SAVE STATE
# ---------------------------------------------------------
def load_state():
    if os.path.exists(SAVE_PATH):
        try:
            with open(SAVE_PATH, "r", encoding="utf8") as f:
                data = json.load(f)
            with STATE_LOCK:
                STATE.update(data)
            print("[server] Loaded state.json")
        except Exception as e:
            print("[server] Failed to load state:", e)

def save_state():
    try:
        os.makedirs(SAVE_DIR, exist_ok=True)
        with open(SAVE_PATH, "w", encoding="utf8") as f:
            with STATE_LOCK:
                json.dump(STATE, f, indent=4)
    except Exception as e:
        print("[server] Failed to save state:", e)

# ---------------------------------------------------------
# ORIGINAL XP HTML
# ---------------------------------------------------------
@app.route("/")
def index():
    return render_template("index.html")

# ---------------------------------------------------------
# ROUTES — STATE
# ---------------------------------------------------------
@app.route("/api/state")
def api_state():
    with STATE_LOCK:
        return jsonify(STATE)

# ---------------------------------------------------------
# ROUTES — LOGS
# ---------------------------------------------------------
@app.route("/api/log", methods=["POST"])
def api_log():
    msg = request.json.get("msg", "")
    add_log(msg)
    return jsonify({"ok": True})

@app.route("/api/logs")
def api_logs():
    with STATE_LOCK:
        return jsonify(STATE["logs"])

# ---------------------------------------------------------
# ROUTES — LEGACY BOTCMD (AutoIt compatibility)
# ---------------------------------------------------------
@app.route("/api/legacy/botcmd", methods=["POST"])
def api_legacy_botcmd():
    cmd = request.json.get("cmd", "")
    add_log(f"[LegacyBotCmd] {cmd}")
    socketio.emit("legacy_cmd", {"cmd": cmd})
    return jsonify({"ok": True})

# ---------------------------------------------------------
# ROUTES — LEGACY MOVEMENT COMMANDS
# ---------------------------------------------------------
LEGACY_MOVEMENT_MAP = {
    "move_forward": {"action": "move", "dir": "forward"},
    "move_backward": {"action": "move", "dir": "backward"},
    "turn_left": {"action": "turn", "dir": "left"},
    "turn_right": {"action": "turn", "dir": "right"},
    "jump": {"action": "jump"},
}

@app.route("/api/legacy/move", methods=["POST"])
def api_legacy_move():
    cmd = request.json.get("cmd", "")
    mapped = LEGACY_MOVEMENT_MAP.get(cmd)

    if mapped:
        add_log(f"[LegacyMove] {cmd}")
        socketio.emit("legacy_move", mapped)
        return jsonify({"ok": True})

    return jsonify({"error": "unknown legacy movement command"}), 400

# ---------------------------------------------------------
# ROUTES — BOTS
# ---------------------------------------------------------
@app.route("/api/bots")
def api_bots():
    with STATE_LOCK:
        return jsonify(STATE["bots"])

@app.route("/api/bots/update", methods=["POST"])
def api_bots_update():
    data = request.json
    update_bots(data)
    return jsonify({"ok": True})

@app.route("/api/bots/register", methods=["POST"])
def api_bots_register():
    data = request.json
    name = data.get("name")
    if not name:
        return jsonify({"error": "missing name"}), 400

    with STATE_LOCK:
        STATE["bots"][name] = {
            "status": "online",
            "last_seen": time.time(),
            "data": data
        }

    socketio.emit("bot_join", {name: STATE["bots"][name]})
    save_state()
    return jsonify({"ok": True})

# ---------------------------------------------------------
# NEW — BOT START/STOP ENDPOINTS
# ---------------------------------------------------------
@app.route("/api/start_bot", methods=["POST"])
def api_start_bot():
    data = request.json or {}
    name = data.get("name", "Bot1")

    add_log(f"[BotStart] Request to start bot: {name}")

    socketio.emit("bot_start", {"name": name})

    with STATE_LOCK:
        STATE["bots"].setdefault(name, {})
        STATE["bots"][name]["status"] = "starting"
        STATE["bots"][name]["last_seen"] = time.time()

    save_state()
    return jsonify({"status": "starting", "bot": name})


@app.route("/api/stop_bot", methods=["POST"])
def api_stop_bot():
    data = request.json or {}
    name = data.get("name", "Bot1")

    add_log(f"[BotStop] Request to stop bot: {name}")

    socketio.emit("bot_stop", {"name": name})

    with STATE_LOCK:
        if name in STATE["bots"]:
            STATE["bots"][name]["status"] = "stopping"

    save_state()
    return jsonify({"status": "stopping", "bot": name})

# ---------------------------------------------------------
# ROUTES — MAP
# ---------------------------------------------------------
@app.route("/api/map")
def api_map():
    with STATE_LOCK:
        return jsonify(STATE["map"])

@app.route("/api/map/update", methods=["POST"])
def api_map_update():
    data = request.json
    update_map(data)
    return jsonify({"ok": True})

# ---------------------------------------------------------
# ROUTES — PERSONALITY
# ---------------------------------------------------------
@app.route("/api/personality")
def api_personality():
    with STATE_LOCK:
        return jsonify(STATE["personality"])

@app.route("/api/personality/update", methods=["POST"])
def api_personality_update():
    data = request.json
    update_personality(data)
    save_state()
    return jsonify({"ok": True})

# ---------------------------------------------------------
# ROUTES — SETTINGS
# ---------------------------------------------------------
@app.route("/api/settings")
def api_settings():
    with STATE_LOCK:
        return jsonify(STATE["settings"])

@app.route("/api/settings/update", methods=["POST"])
def api_settings_update():
    data = request.json
    update_settings(data)
    save_state()
    return jsonify({"ok": True})

# ---------------------------------------------------------
# UPDATE FUNCTIONS (broadcast to WebSocket)
# ---------------------------------------------------------
def update_bots(bots):
    with STATE_LOCK:
        if isinstance(bots, list):
            converted = {}
            for entry in bots:
                name = entry.get("name", "Unknown")
                converted[name] = {
                    "status": "online",
                    "last_seen": time.time(),
                    "data": entry,
                }
            bots = converted

        for name, data in bots.items():
            STATE["bots"][name] = data
            STATE["bots"][name]["last_seen"] = time.time()

    socketio.emit("bots_update", STATE["bots"])
    save_state()

def update_map(map_data):
    with STATE_LOCK:
        if isinstance(map_data, list) and len(map_data) == 2 and isinstance(map_data[0], (int, float)):
            map_data = [{
                "x": map_data[0],
                "y": map_data[1],
                "name": "Unknown"
            }]

        STATE["map"] = map_data

    socketio.emit("map_update", STATE["map"])
    save_state()

def update_personality(data):
    if isinstance(data, str):
        data = {"text": data}

    with STATE_LOCK:
        STATE["personality"] = data

    socketio.emit("personality_update", STATE["personality"])
    save_state()

def update_settings(data):
    if isinstance(data, dict) and any("=" in k for k in data.keys()):
        converted = {}
        for k, v in data.items():
            key = k.split("=")[0].strip()
            val = k.split("=")[1].strip()
            converted[key] = val
        data = converted

    with STATE_LOCK:
        STATE["settings"] = data

    socketio.emit("settings_update", STATE["settings"])
    save_state()

def add_log(msg):
    with STATE_LOCK:
        STATE["logs"].append(msg)
        STATE["logs"] = STATE["logs"][-500:]
    socketio.emit("log_update", msg)
    save_state()

# ---------------------------------------------------------
# LEGACY FILE WATCHERS
# ---------------------------------------------------------
LEGACY_CMD_FILE = "botcmd.txt"
LEGACY_STATE_FILE = "botstate.txt"

def legacy_file_watcher():
    last_cmd = ""
    last_state = ""

    while True:
        if os.path.exists(LEGACY_CMD_FILE):
            try:
                with open(LEGACY_CMD_FILE, "r", encoding="utf8") as f:
                    cmd = f.read().strip()
                if cmd and cmd != last_cmd:
                    last_cmd = cmd
                    add_log(f"[LegacyFileCmd] {cmd}")
                    socketio.emit("legacy_cmd", {"cmd": cmd})
            except:
                pass

        if os.path.exists(LEGACY_STATE_FILE):
            try:
                with open(LEGACY_STATE_FILE, "r", encoding="utf8") as f:
                    raw = f.read().strip()
                if raw and raw != last_state:
                    last_state = raw
                    try:
                        data = json.loads(raw)
                        update_bots(data)
                    except:
                        update_bots({"LegacyBot": {"text": raw}})
            except:
                pass

        time.sleep(0.5)

threading.Thread(target=legacy_file_watcher, daemon=True).start()

# ---------------------------------------------------------
# HEARTBEAT — bot online/offline detection
# ---------------------------------------------------------
def heartbeat():
    while True:
        now = time.time()
        offline = []

        with STATE_LOCK:
            for name, bot in STATE["bots"].items():
                if now - bot.get("last_seen", 0) > 5:
                    bot["status"] = "offline"
                    offline.append(name)

        if offline:
            socketio.emit("bots_update", STATE["bots"])

        socketio.emit("state_update", STATE)
        time.sleep(1)

threading.Thread(target=heartbeat, daemon=True).start()

# ---------------------------------------------------------
# MAIN ENTRY POINT
# ---------------------------------------------------------
def start_server(ip="0.0.0.0", port=5000):
    print(f"[server] Starting Web‑UI at http://{ip}:{port}")
    load_state()
    socketio.run(app, host=ip, port=port)
