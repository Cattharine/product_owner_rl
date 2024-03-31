from empirical_reward_system import EmpiricalRewardSystem

PURCHASE_ACTIONS = {3, 4, 5, 6}
LATE_PURCHASE_SPRINT = 29

class EmpiricalCreditStageRewardSystem(EmpiricalRewardSystem):
    def get_reward(self, state_old, action, state_new) -> float:
        reward = super().get_reward(state_old, action, state_new)
        reward += self.get_credit_payer_reward()
        reward += self.get_late_purchases_punishment(state_old, action, state_new)
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

    def get_late_purchases_punishment(self, state_old, action, state_new) -> float:
        money_diff = self.get_money(state_old) - self.get_money(state_new)
        if money_diff >= 0:
            return 0
        if self.get_sprint(state_new) < LATE_PURCHASE_SPRINT:
            return 0
        if action not in PURCHASE_ACTIONS:
            return 0
        return -100
        