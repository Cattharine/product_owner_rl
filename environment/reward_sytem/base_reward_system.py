class BaseRewardSystem:
    def __init__(self, config: dict) -> None:
        self.sprint_index = 0
        self.money_index = 1
        self.credit_index = 4
        self.done_index = 15
        self.config = config
    
    def get_reward(self, state_old, action, state_new) -> float:
        pass

    def get_credit(self, state) -> float:
        return state[self.credit_index]
    
    def get_money(self, state) -> float:
        return state[self.money_index]
    
    def get_done(self, state) -> bool:
        done_int = state[self.done_index]
        return bool(done_int)
