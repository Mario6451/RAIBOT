# ai/ai_debug_console.py

import time

class AIDebugConsole:
    def __init__(self, profiler):
        self.profiler = profiler
        self.last_print = 0
        self.interval = 0.5

    def print_bot(self, bot):
        print(f"[BOT] {bot.name}")
        print(f"  Pos: ({bot.x:.1f}, {bot.z:.1f})")
        print(f"  Yaw: {bot.yaw:.1f}")
        print(f"  Mode: {bot.mode}")
        print(f"  Target: {bot.target}")
        print(f"  Path length: {len(bot.pathfinder.current_path)}")
        print(f"  Stuck: {bot.stuck}")

    def print_profiler(self):
        print(f"[PROFILER] avg={self.profiler.avg_tick_ms():.2f}ms "
              f"max={self.profiler.max_tick_ms():.2f}ms "
              f"TPS={self.profiler.tps():.1f}")

    def tick(self, world):
        now = time.time()
        if now - self.last_print < self.interval:
            return

        print("\n=== AI DEBUG ===")
        for bot in world.bots:
            self.print_bot(bot)

        self.print_profiler()

        self.last_print = now
