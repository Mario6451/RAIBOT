import tkinter as tk
from settings import load_settings
from ui.settings.settings_ui import SettingsUI


def main():
    settings = load_settings()

    root = tk.Tk()
    root.title("AI Bot Settings")

    SettingsUI(root, settings)

    root.mainloop()

if __name__ == "__main__":
    main()
