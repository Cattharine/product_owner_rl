from game.userstory_card.userstory_card_info import UserStoryCardInfo


class BugUserStoryInfo(UserStoryCardInfo):
    def __init__(self, spawn_sprint):
        super().__init__(label_val="Bug", spawn_sprint=spawn_sprint)
        self.loyalty_debuff = -0.05
        self.loyalty_increment = -0.05
        self.customers_debuff = -0.5
        self.customers_increment = -0.5
