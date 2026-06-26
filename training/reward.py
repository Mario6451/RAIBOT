# training/reward.py

class RewardSystem:
    def reward_move(self, success, stuck):
        if stuck:
            return -5
        if success:
            return 3
        return -1

    def reward_chat(self, correct):
        return 2 if correct else -2

    def reward_explore(self, new_area):
        return 1 if new_area else 0
