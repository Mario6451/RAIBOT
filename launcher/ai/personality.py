import random

class PersonalityModule:
    def __init__(self):
        self.chaos = random.uniform(0.2, 0.8)
        self.energy = random.uniform(0.3, 0.9)
        self.friendliness = random.uniform(0.4, 0.9)

    def describe(self):
        return (
            f"chaos={self.chaos:.2f}, "
            f"energy={self.energy:.2f}, "
            f"friendliness={self.friendliness:.2f}"
        )
