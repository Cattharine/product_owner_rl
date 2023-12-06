from typing import Any
from enum import Enum
from copy import copy
import random


UserCardType = Enum("UserCardType", ["S", "M", "L", "XL", "BUG", "TECH_DEBT"])
UserCardColor = Enum("UserCardColor",
                     ["BLUE", "GREEN", "ORANGE", "PINK", "PURPLE", "RED", "YELLOW"])
colors_for_use = [UserCardColor.BLUE, UserCardColor.GREEN, UserCardColor.ORANGE,
                  UserCardColor.PINK, UserCardColor.PURPLE, UserCardColor.RED,
                  UserCardColor.YELLOW]


project_name = ""

used_colors = {UserCardType.S: [], UserCardType.M: [], UserCardType.L: [],
               UserCardType.XL: [], UserCardType.BUG: [], UserCardType.TECH_DEBT: []}

AMOUNT_CREDIT_PAYMENT = 9000

BLANK_SPRINT_LOYALTY_DECREMENT = {
    6: -0.05,
    9: -0.1,
    12: -0.15
}
min_key_blank_sprint_loyalty = min(BLANK_SPRINT_LOYALTY_DECREMENT.keys())

BLANK_SPRINT_CUSTOMERS_DECREMENT = {
    6: -0.5,
    9: -1.0,
    12: -1.5
}

USERSTORY_FLOATING_PROFIT = {3: [1, 1.3], 6: [0.7, 0.9], 9: [0.2, 0.6], 12: [-0.2, 0.1]}
sorted_keys_userstory_floating_profit = sorted(USERSTORY_FLOATING_PROFIT.keys())

statistical_research_cost = 80000

BUG_SPAM_PROBABILITY = 0.25
TECH_DEBT_SPAWN_PROBABILITY = 0.5



def reload_game():
    global used_colors
    for i in used_colors.keys():
        used_colors[i] = []


def get_unused_color(uc_type: UserCardType):
    global used_colors
    if len(used_colors[uc_type]) == 7:
        print("Не осталось не использованных цветов.")
        return
    # todo в Godot'е и python используются разные генераторы (псевдо-)случайных чисел
    cfu = copy(colors_for_use)
    for i in used_colors[uc_type]:
        cfu.remove(i)
    i = random.randint(0, len(cfu) - 1)
    color = cfu[i]
    used_colors[uc_type].append(color)
    return color


def release_color(us_type: UserCardType, color: UserCardColor):
    global used_colors
    used_colors[us_type].remove(color)


def interpolate(value, table: dict):
    keys = sorted(table.keys())
    first_key = keys[0]
    if value <= first_key:
        return table[first_key]

    last_key = keys[-1]
    if value >= last_key:
        return table[last_key]

    for i in range(1, len(keys)):
        if keys[i - 1] < value <= keys[i]:
            a = table[keys[i - 1]]
            b = table[keys[i]]
            u = a + (value - keys[i - 1]) * (b - a) / (keys[i] - keys[i - 1])
            return u

    return None
