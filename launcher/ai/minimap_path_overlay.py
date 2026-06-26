# ui/minimap_path_overlay.py

from ai.path_visualizer import PathVisualizer

class MinimapPathOverlay:
    def __init__(self, minimap):
        self.minimap = minimap
        self.visualizer = PathVisualizer(minimap.surface)

    def render_bot_path(self, bot):
        if bot.pathfinder.current_path:
            self.visualizer.draw_path(bot.pathfinder.current_path)
