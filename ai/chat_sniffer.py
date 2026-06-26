# ai/chat_sniffer.py

import re
import time

class ChatSniffer:
    def __init__(self, memory_reader=None, ocr_reader=None):
        """
        memory_reader: object with .read_chat() -> str | None
        ocr_reader:    object with .read_chat() -> str | None
        """
        self.memory_reader = memory_reader
        self.ocr_reader = ocr_reader

        self.last_msg = None
        self.last_time = 0

    def get_latest_message(self):
        """
        Returns the newest chat message or None.
        Priority:
        1. Memory
        2. OCR
        """
        msg = None

        # Try memory first
        if self.memory_reader:
            try:
                msg = self.memory_reader.read_chat()
            except:
                msg = None

        # Fallback to OCR
        if msg is None and self.ocr_reader:
            try:
                msg = self.ocr_reader.read_chat()
            except:
                msg = None

        # No new message
        if not msg or msg == self.last_msg:
            return None

        self.last_msg = msg
        self.last_time = time.time()

        # Strip "PlayerName: message"
        msg = re.sub(r"^\w+:\s*", "", msg)
        return msg
