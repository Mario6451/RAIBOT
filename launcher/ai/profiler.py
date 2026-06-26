# ai/profiler.py

import time

class AIProfiler:
    def __init__(self):
        self.last_tick = time.time()
        self.tick_times = []
        self.max_samples = 120  # last 2 seconds at 60 FPS

    def start_tick(self):
        self._tick_start = time.time()

    def end_tick(self):
        now = time.time()
        dt = now - self._tick_start
        self.tick_times.append(dt)

        if len(self.tick_times) > self.max_samples:
            self.tick_times.pop(0)

        self.last_tick = now

    # ---------------------------------------------------------
    # METRICS
    # ---------------------------------------------------------
    def avg_tick_ms(self):
        if not self.tick_times:
            return 0
        return (sum(self.tick_times) / len(self.tick_times)) * 1000

    def max_tick_ms(self):
        if not self.tick_times:
            return 0
        return max(self.tick_times) * 1000

    def tps(self):
        if not self.tick_times:
            return 0
        avg = sum(self.tick_times) / len(self.tick_times)
        return 1.0 / avg

    # ---------------------------------------------------------
    # DEBUG PRINT
    # ---------------------------------------------------------
    def debug_print(self):
        print(
            f"AI Tick: avg={self.avg_tick_ms():.2f}ms | "
            f"max={self.max_tick_ms():.2f}ms | "
            f"TPS={self.tps():.1f}"
        )
