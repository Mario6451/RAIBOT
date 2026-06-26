import tkinter as tk
from tkinter import ttk

class PersonalityUI(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        ttk.Label(self, text="(Future) Personality Controls").pack(pady=20)
        ttk.Label(self, text="Sliders for chaos, friendliness, energy, etc.").pack()
