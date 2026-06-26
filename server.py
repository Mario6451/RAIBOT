# server.py — BACKWARDS COMPATIBILITY SHIM

from dashboard.server import (
    start_server,
    update_bots,
    update_map,
    update_personality,
    update_settings,
    add_log,
    STATE,
)

__all__ = [
    "start_server",
    "update_bots",
    "update_map",
    "update_personality",
    "update_settings",
    "add_log",
    "STATE",
]
