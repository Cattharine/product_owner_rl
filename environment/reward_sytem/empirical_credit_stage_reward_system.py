from empirical_reward_system import EmpiricalRewardSystem

class EmpiricalCreditStageRewardSystem(EmpiricalRewardSystem):
    def get_reward(self, state_old, action, state_new) -> float:
        reward = super().get_reward(state_old, action, state_new)
        reward += self.get_credit_payer_reward()
        return reward

    def get_credit_payer_reward(self, state_old, state_new) -> float:
        potential_old = self.get_potential(state_old)
        potential_new = self.get_potential(state_new)

        diff = (potential_new - potential_old) * 3
        return diff

    def get_potential(self, state):
        loyalty = self.get_loyalty(state)
        customers = self.get_customers(state)

        potential = loyalty * customers
        return potential

    def get_late_purchases_punishment(self):
        pass