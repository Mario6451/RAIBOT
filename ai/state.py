# ai/state.py

class BotState:
    """
    Stores the bot's current state and pending AutoIt commands.
    """

    def __init__(self):
        self.pending_command = None

        self.last_action = None
        self.last_move = None
        self.last_chat = None

        self.is_afk = False
        self.is_stuck = False
        self.is_moving = False

        self.last_player_pos = None
        self.last_chat_message = None

        self.mood = "neutral"
        self.confidence = 0.5

    def set_command(self, cmd: dict):
        self.pending_command = cmd
        self.last_action = cmd.get("type")
