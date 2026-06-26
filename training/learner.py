# training/learner.py

class Learner:
    def __init__(self, memory, stats, rewarder):
        self.memory = memory
        self.stats = stats
        self.rewarder = rewarder

    def learn_from_action(self, action, result):
        reward = 0

        if action == "move_to":
            reward = self.rewarder.reward_move(
                result.get("success", False),
                result.get("stuck", False)
            )

        elif action == "say":
            reward = self.rewarder.reward_chat(
                result.get("correct", False)
            )

        elif action == "explore":
            reward = self.rewarder.reward_explore(
                result.get("new_area", False)
            )

        # Apply reward to stats
        self.stats.apply_reward(reward)

        # Log memory
        self.memory.log({
            "action": action,
            "reward": reward,
            "result": result
        })
