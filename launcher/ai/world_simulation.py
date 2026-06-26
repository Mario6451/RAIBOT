# ai/world_simulation.py

import time

class WorldSimulation:
    def __init__(self, world, behavior_tree, enemy_ai, profiler):
        self.world = world
        self.behavior_tree = behavior_tree
        self.enemy_ai = enemy_ai
        self.profiler = profiler
        self.running = True

    def tick(self):
        self.profiler.start_tick()

        # Update bots
        for bot in self.world.bots:
            self.behavior_tree.tick(bot)

        # Update enemies
        for enemy in self.world.enemies:
            self.enemy_ai.tick(enemy)

        self.profiler.end_tick()

    def run(self, tick_rate=60):
        delay = 1.0 / tick_rate

        while self.running:
            start = time.time()
            self.tick()
            elapsed = time.time() - start

            sleep_time = delay - elapsed
            if sleep_time > 0:
                time.sleep(sleep_time)
