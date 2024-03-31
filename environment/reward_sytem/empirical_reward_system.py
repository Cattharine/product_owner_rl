from .base_reward_system import BaseRewardSystem

class EmpiricalRewardSystem(BaseRewardSystem):
    def get_reward(self, state_old, action, state_new) -> float:
        if (state_old == state_new).all():
            return -10
        reward = 0
        if self.get_credit(state_old) > 0 and self.get_credit(state_new) <= 0:
            reward += 10
        reward += self.get_done_reward(state_new)
        reward += self.get_action_reward(state_old, action, state_new)

        return reward

    def get_done_reward(self, state_new) -> float:
        done = self.get_done(state_new)
        if not done:
            return 0
        if self.get_money(state_new) > 10:
            return 500
        return -50
    
    def get_action_reward(self, state_old, action, state_new) -> float:
        if action in self.config['remove_sprint_card_actinos']:
            return -2
        return 1