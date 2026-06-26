# bot/bot_launcher.py
# 2016 Roblox Client Launcher (future-proof for multi-version support)

import os
import subprocess
import urllib.parse
import json
import threading
import webbrowser


# ---------------------------------------------------------
# SETTINGS LOADER
# ---------------------------------------------------------
def load_settings():
    path = os.path.join("settings", "launcher.json")

    # Default fallback
    defaults = {
        "client_path": "",
        "joinscript_url": "https://www.rbolock.tk/game/join2017.php",
        "place_id": "0",
        "web_ui_port": 5000,
        "version": "2016"   # NEW: version selector for multi-version support
    }

    if not os.path.exists(path):
        return defaults

    with open(path, "r", encoding="utf8") as f:
        data = json.load(f)

    # Ensure all keys exist
    for k, v in defaults.items():
        data.setdefault(k, v)

    return data


# ---------------------------------------------------------
# DASHBOARD SERVER CONTROL
# ---------------------------------------------------------
def start_web_ui_server(port: int):
    try:
        subprocess.Popen(
            ["python", "server.py", "--port", str(port)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        print(f"[launcher] Web UI server started on port {port}")
    except Exception as e:
        print(f"[launcher] Failed to start Web UI server: {e}")


def open_web_ui(port: int):
    url = f"http://localhost:{port}"
    print(f"[launcher] Opening Web UI: {url}")
    webbrowser.open(url)


# ---------------------------------------------------------
# JOIN URL BUILDER (2016-compatible)
# ---------------------------------------------------------
def build_join_url(base_url, place_id, ip, port, user_id, username, membership, avatar_binary):
    """
    2016 Roblox clients ONLY use join URL parameters.
    """
    params = {
        "placeid": place_id,
        "ip": ip,
        "port": port,
        "user": username,
        "id": user_id,
        "mship": membership,
        "binary": avatar_binary
    }

    return base_url + "?" + urllib.parse.urlencode(params)


# ---------------------------------------------------------
# CLIENT LAUNCHER (2016-compatible)
# ---------------------------------------------------------
def launch_client_2016(executable_path, join_url):
    """
    Launches a 2016 Roblox client using ONLY the flags it supports.
    """
    if not os.path.exists(executable_path):
        raise FileNotFoundError(f"Roblox client not found: {executable_path}")

    args = [
        executable_path,
        "-a", "http://rbolock.tk/login/Negotiate.php",
        "-j", join_url,
        "-t", "1"
    ]

    print("[bot_launcher] Launching 2016 client:")
    print(" ".join(args))

    subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


# ---------------------------------------------------------
# MULTI-VERSION SUPPORT (future-proof)
# ---------------------------------------------------------
def launch_client(executable_path, join_url, version="2016"):
    """
    Wrapper for multi-version Roblox client support.
    """
    if version == "2016":
        return launch_client_2016(executable_path, join_url)

    # Future versions can be added here:
    # elif version == "2017":
    #     return launch_client_2017(...)
    # elif version == "2018":
    #     return launch_client_2018(...)

    raise ValueError(f"Unsupported Roblox version: {version}")


# ---------------------------------------------------------
# MAIN ENTRY POINT
# ---------------------------------------------------------
def main():
    settings = load_settings()
    port = settings.get("web_ui_port", 5000)

    # Start dashboard server
    threading.Thread(target=start_web_ui_server, args=(port,), daemon=True).start()
    open_web_ui(port)

    print("[launcher] Ready. Use build_join_url() + launch_client() to start bots.")


if __name__ == "__main__":
    main()
