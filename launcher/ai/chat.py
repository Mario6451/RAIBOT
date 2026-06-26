# ai/chat.py

import random

class ChatModule:
    def __init__(self, settings):
        self.settings = settings
        self.last_reply = ""

    def generate_reply(self, msg: str) -> str:
        msg = msg.lower()

        if "hi" in msg or "hello" in msg:
            return random.choice(["hi", "hello!", "hey"])
        if "follow" in msg:
            return "ok"
        if "where" in msg and "you" in msg:
            return "just exploring"

        return random.choice(["ok", "sure", "alright", "hmm"])

    def send(self, text: str):
        return {
            "type": "chat",
            "text": text
        }
