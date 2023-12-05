from game.userstory_card.userstory_card import UserStoryCard
from game.userstory_card.userstory_card_info import UserStoryCardInfo
import random


class UserStoriesGenerator:
    def __init__(self, s: int, m: int, l: int, xl: int):
        self.a = []
        sizes_count = [[s, "S"], [m, "M"], [l, "L"], [xl, "XL"]]
        for size in sizes_count:
            self.a += [size[1]] * size[0]

    def generate_userstories(self, count: int, spawn_sprint: int):
        result = []

        for i in range(count):
            card_type = self.a[random.randint(0, len(self.a) - 1)]
            card = UserStoryCard(UserStoryCardInfo(card_type, spawn_sprint))

            result.append(card)

        return result
