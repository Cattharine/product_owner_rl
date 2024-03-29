from empirical_reward_system import EmpiricalRewardSystem

class EmpiricalCreditStageRewardSystem(EmpiricalRewardSystem):
    def get_reward(self, state_old, action, state_new) -> float:
        reward = super().get_reward(state_old, action, state_new)

    def credit_payer_reward(self):
        pass

    def get_late_purchases_punishment(self):
        pass