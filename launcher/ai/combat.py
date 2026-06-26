# ai/combat.py

import time

class Combat:
    def __init__(self, movement, sensors):
        self.movement = movement
        self.sensors = sensors
        self.cooldowns = {}

    def _ready(self, bot, ability):
        now = time.time()
        cd = self.cooldowns.get((bot.name, ability), 0)
        return now >= cd

    def _set_cd(self, bot, ability, seconds):
        self.cooldowns[(bot.name, ability)] = time.time() + seconds

    # Basic attack
    def attack(self, bot, target):
        if not self._ready(bot, "attack"):
            return

        # Move toward target
        self.movement.move_to(target.x, target.z)

        # Trigger attack animation
        self.movement.left_click()

        # Set cooldown
        self._set_cd(bot, "attack", 0.8)

    # Auto-attack behavior
    def tick(self, bot):
        enemy = self.sensors.get_closest_enemy(bot)
        if enemy:
            self.attack(bot, enemy)
