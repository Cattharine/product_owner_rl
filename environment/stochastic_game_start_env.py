from environment.environment import ProductOwnerEnv
from game.game_generators import (
    ProductOwnerGame,
    get_buggy_game_1,
    get_buggy_game_2,
    get_buggy_game_3,
    get_game_on_sprint_6,
    get_game_on_sprint_21,
    get_game_on_sprint_26,
)


class StochasticGameStartEnv(ProductOwnerEnv):
    def __init__(
        self,
        userstories_env=None,
        backlog_env=None,
        with_info=True,
        seed=None,
        card_picker_seed=None
    ):
        super().__init__(
            userstories_env,
            backlog_env,
            with_info,
            seed=seed,
            card_picker_seed=card_picker_seed
        )

        self.index = 0
        self.generators = [
            ProductOwnerGame,
            get_game_on_sprint_6,
            get_game_on_sprint_21,
            get_game_on_sprint_26,
            get_buggy_game_1,
            get_buggy_game_2,
            get_buggy_game_3,
        ]

    def reset(self, seed=None, card_picker_seed=None):
        self.game = self.generators[self.index](seed)
        super()._reset_card_picker_random_generator(card_picker_seed)
        self.index = (self.index + 1) % len(self.generators)
        self.current_state = self._get_state()
        return self.current_state
