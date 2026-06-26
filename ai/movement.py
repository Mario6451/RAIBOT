# ai/movement.py

import random
import json

class MovementController:
    def __init__(self, stats):
        self.stats = stats
        self.state = None  # set by AIBrain

    # ---------------------------------------------------------
    # INTERNAL: queue a JSON command for AutoIt
    # ---------------------------------------------------------
    def _send(self, payload: dict):
        """
        Instead of sending raw strings, we store a JSON object
        in state.pending_command. bot_runtime will write it to
        botcmd.txt for AutoIt to consume.
        """
        if self.state is None:
            return

        # JSON encode the command
        self.state.pending_command = json.dumps(payload)

    # ---------------------------------------------------------
    # MOVEMENT ACTIONS (AutoIt JSON)
    # ---------------------------------------------------------

    def move_to(self, target, style):
        """
        AutoIt handles the actual movement.
        We only send the JSON command.
        """
        x, y, z = target
        self._send({
            "type": "move_to",
            "x": x,
            "y": y,
            "z": z,
            "style": style
        })
        return True, False  # success, stuck

    def random_explore(self, style):
        self._send({
            "type": "explore",
            "style": style
        })
        return True

    def circle_player(self, player):
        pos = player["pos"]
        self._send({
            "type": "circle_player",
            "x": pos[0],
            "y": pos[1],
            "z": pos[2]
        })
        return pos

    def back_away(self, player):
        pos = player["pos"]
        self._send({
            "type": "back_away",
            "x": pos[0],
            "y": pos[1],
            "z": pos[2]
        })
        return pos

    def peek_corner(self):
        self._send({"type": "peek"})

    def combat_move(self, player):
        pos = player["pos"]
        self._send({
            "type": "combat_move",
            "x": pos[0],
            "y": pos[1],
            "z": pos[2]
        })

    def shiftlock_wiggle(self):
        self._send({"type": "shiftlock_wiggle"})
