from ui.ui_main import LauncherUI
from controller.controller_main import LauncherController

def run_launcher():
    ui = LauncherUI()
    controller = LauncherController(ui)
    ui.root.mainloop()

if __name__ == "__main__":
    run_launcher()
