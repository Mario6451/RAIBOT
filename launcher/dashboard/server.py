# dashboard/server.py — compact full-feature version

from flask import Flask, jsonify, request, render_template
from flask_socketio import SocketIO
import threading, time, json, os

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="threading")

STATE = {
    "bots": {},
    "map": [],
    "logs": [],
    "personality": {},
    "settings": {},
}
LOCK = threading.Lock()
SAVE_DIR = "dashboard"
SAVE_PATH = os.path.join(SAVE_DIR, "state.json")
LEGACY_CMD_FILE = "botcmd.txt"
LEGACY_STATE_FILE = "botstate.txt"


def _with_lock(fn):
    def wrapper(*args, **kwargs):
        with LOCK:
            return fn(*args, **kwargs)
    return wrapper


def load_state():
    if os.path.exists(SAVE_PATH):
        try:
            with open(SAVE_PATH, "r", encoding="utf8") as f:
                data = json.load(f)
            with LOCK:
                STATE.update(data)
            print("[server] Loaded state.json")
        except Exception as e:
            print("[server] Failed to load state:", e)


@_with_lock
def save_state():
    try:
        os.makedirs(SAVE_DIR, exist_ok=True)
        with open(SAVE_PATH, "w", encoding="utf8") as f:
            json.dump(STATE, f, indent=4)
    except Exception as e:
        print("[server] Failed to save state:", e)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/state")
def api_state():
    with LOCK:
        return jsonify(STATE)


@app.route("/api/log", methods=["POST"])
def api_log():
    msg = request.json.get("msg", "")
    add_log(msg)
    return jsonify({"ok": True})


@app.route("/api/logs")
def api_logs():
    with LOCK:
        return jsonify(STATE["logs"])


@app.route("/api/legacy/botcmd", methods=["POST"])
def api_legacy_botcmd():
    cmd = request.json.get("cmd", "")
    add_log(f"[LegacyBotCmd] {cmd}")
    socketio.emit("legacy_cmd", {"cmd": cmd})
    return jsonify({"ok": True})


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
    if not mapped:
        return jsonify({"error": "unknown legacy movement command"}), 400
    add_log(f"[LegacyMove] {cmd}")
    socketio.emit("legacy_move", mapped)
    return jsonify({"ok": True})


@app.route("/api/bots")
def api_bots():
    with LOCK:
        return jsonify(STATE["bots"])


@app.route("/api/bots/update", methods=["POST"])
def api_bots_update():
    update_bots(request.json)
    return jsonify({"ok": True})


@app.route("/api/bots/register", methods=["POST"])
def api_bots_register():
    data = request.json
    name = data.get("name")
    if not name:
        return jsonify({"error": "missing name"}), 400
    with LOCK:
        STATE["bots"][name] = {
            "status": "online",
            "last_seen": time.time(),
            "data": data,
        }
    socketio.emit("bot_join", {name: STATE["bots"][name]})
    save_state()
    return jsonify({"ok": True})


@app.route("/api/start_bot", methods=["POST"])
def api_start_bot():
    data = request.json or {}
    name = data.get("name", "Bot1")
    add_log(f"[BotStart] Request to start bot: {name}")
    socketio.emit("bot_start", {"name": name})
    with LOCK:
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
    with LOCK:
        if name in STATE["bots"]:
            STATE["bots"][name]["status"] = "stopping"
    save_state()
    return jsonify({"status": "stopping", "bot": name})


@app.route("/api/map")
def api_map():
    with LOCK:
        return jsonify(STATE["map"])


@app.route("/api/map/update", methods=["POST"])
def api_map_update():
    update_map(request.json)
    return jsonify({"ok": True})


@app.route("/api/personality")
def api_personality():
    with LOCK:
        return jsonify(STATE["personality"])


@app.route("/api/personality/update", methods=["POST"])
def api_personality_update():
    update_personality(request.json)
    save_state()
    return jsonify({"ok": True})


@app.route("/api/settings")
def api_settings():
    with LOCK:
        return jsonify(STATE["settings"])


@app.route("/api/settings/update", methods=["POST"])
def api_settings_update():
    update_settings(request.json)
    save_state()
    return jsonify({"ok": True})


@_with_lock
def update_bots(bots):
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


@_with_lock
def update_map(map_data):
    if isinstance(map_data, list) and len(map_data) == 2 and isinstance(map_data[0], (int, float)):
        map_data = [{"x": map_data[0], "y": map_data[1], "name": "Unknown"}]
    STATE["map"] = map_data
    socketio.emit("map_update", STATE["map"])
    save_state()


@_with_lock
def update_personality(data):
    if isinstance(data, str):
        data = {"text": data}
    STATE["personality"] = data
    socketio.emit("personality_update", STATE["personality"])
    save_state()


@_with_lock
def update_settings(data):
    if isinstance(data, dict) and any("=" in k for k in data.keys()):
        converted = {}
        for k, v in data.items():
            key, val = k.split("=", 1)
            converted[key.strip()] = val.strip()
        data = converted
    STATE["settings"] = data
    socketio.emit("settings_update", STATE["settings"])
    save_state()


@_with_lock
def add_log(msg):
    STATE["logs"].append(msg)
    STATE["logs"] = STATE["logs"][-500:]
    socketio.emit("log_update", msg)
    save_state()


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


def heartbeat():
    while True:
        now = time.time()
        offline = []
        with LOCK:
            for name, bot in STATE["bots"].items():
                if now - bot.get("last_seen", 0) > 5:
                    bot["status"] = "offline"
                    offline.append(name)
        if offline:
            socketio.emit("bots_update", STATE["bots"])
        socketio.emit("state_update", STATE)
        time.sleep(1)


threading.Thread(target=legacy_file_watcher, daemon=True).start()
threading.Thread(target=heartbeat, daemon=True).start()


def start_server(ip="0.0.0.0", port=5000):
    print(f"[server] Starting Web‑UI at http://{ip}:{port}")
    load_state()
    socketio.run(app, host=ip, port=port)
