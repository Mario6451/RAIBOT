# launcher/controller/controller_personality.py

import json
import os
from tkinter import filedialog


class PersonalityController:
    def __init__(self, main):
        self.main = main
        self.ui = main.ui
        self.path = "settings/persona.txt"

    def load_persona(self):
        if os.path.exists(self