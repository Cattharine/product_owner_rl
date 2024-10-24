from environment.backlog_env import BacklogEnv
from environment.userstory_env import UserstoryEnv
from environment.environment import ProductOwnerEnv


USUAL_CREDIT_ENV_END_SPRINT = 35
EARLY_CREDIT_ENV_END_SPRINT = 32
LATE_PURCHASE_SPRINT = 29
PURCHASE_ACTIONS = {3, 4, 5, 6}


class CreditPayerEnv(ProductOwnerEnv):
    def __init__(self, userstory_env=None, backlog_env=None, with_end=False,
                 with_info=True, reward_system=None, seed=None, card_picker_seed=None):
        if userstory_env is None:
            userstory_env = UserstoryEnv(6, 0, 0)
        if backlog_env is None:
            backlog_env = BacklogEnv(12, 0, 0, 0, 0, 0)
        super().__init__(userstory_env, backlog_env, with_info, reward_system,
                         seed=seed, card_picker_seed=card_picker_seed)
        self.with_end = with_end
        if self.with_end:
            self.end_sprint = USUAL_CREDIT_ENV_END_SPRINT
        else:
            self.end_sprint = EARLY_CREDIT_ENV_END_SPRINT

    def get_done(self, info):
        done_game = super().get_done(info)
        done_credit = self.game.context.current_sprint == self.end_sprint
        return done_game or done_credit
