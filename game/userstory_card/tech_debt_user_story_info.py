from game.userstory_card.userstory_card_info import UserStoryCardInfo


class TechDebtInfo(UserStoryCardInfo):
    def __init__(self, spawn_sprint):
        super().__init__(label_val="TechDebt", spawn_sprint=spawn_sprint)
        self.hours_debuff_increment = 1
        self.full_hours_debuff = 1
