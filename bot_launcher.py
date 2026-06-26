import os
import subprocess
import urllib.parse
import json
import threading
import webbrowser


def load_settings():
    path = os.path.join("settings", "launcher.json")
    if not os.path.exists(path):
        return {
            "client_path": "",
            "joinscript_url": "https://www.rbolock.tk/game/join2017.php",
            "place_id": "0",
            "web_ui_port": 5000
        }

    with open(path, "r", encoding="utf8") as f:
        data = json.load(f)

    data.setdefault("client_path", "")
    data.setdefault("joinscript_url", "https://www.rbolock.tk/game/join2017.php")
    data.setdefault("place_id", "0")
    data.setdefault("web_ui_port", 5000)

    return data


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


def build_join_url(base_url, place_id, ip, port, user_id, username, membership, avatar_binary):
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


def launch_client(executable_path, join_url):
    if not os.path.exists(executable_path):
        raise FileNotFoundError(f"Roblox client not found: {executable_path}")

    args = [
        executable_path,
        "-a", "http://rbolock.tk/login/Negotiate.php",
        "-j", join_url,
        "-t", "1"
    ]

    print("[bot_launcher] Launching client:")
    print(" ".join(args))

    subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


def main():
    settings = load_settings()
    port = settings.get("web_ui_port", 5000)

    threading.Thread(target=start_web_ui_server, args=(port,), daemon=True).start()
    open_web_ui(port)

    print("[launcher] Ready. Use build_join_url() + launch_client() to start bots.")


if __name__ == "__main__":
    main()
