import tkinter as tk
from settings import load_settings
from launcher.ui.ui_main import MainUI


class MainApp:
    def __init__(self):
        self.settings = load_settings()

        self.root = tk.Tk()
        self.root.title("RAI Launcher")

        self.ui = MainUI(self.root, self)

        self.ui.init_versions()
        self.ui.init_bots()

    def reload_bot_list(self):
        self.ui.init_bots()

    def save_settings(self):
        from settings import save_settings
        save_settings(self.settings.settings)

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = MainApp()
    app.run()
