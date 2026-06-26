def summarize_vision(players, tools, threats):
    summary = {
        "players_detected": len(players),
        "tools_detected": len(tools),
        "threats_detected": len(threats),
        "nearest_player": None
    }

    if players:
        nearest = min(players, key=lambda p: p["area"])
        summary["nearest_player"] = nearest["center"]

    return summary
