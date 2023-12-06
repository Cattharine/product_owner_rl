from game.game_global import UserCardType


class GlobalConstants:
    developer_hours = 10
    statistical_research_cost = 80000
    MONEY_GOAL = 1000000
    MAX_WORKER_COUNT = 4
    NEW_WORKER_COST = 50000
    NEW_ROOM_COST = 200000
    NEW_ROOM_MULTIPLIER = 1.5
    user_survey_cost = 160000

    USERSTORY_LOYALTY = {UserCardType.S: [0.025, 0.08], UserCardType.M: [0.075, 0.175],
                         UserCardType.L: [0.125, 0.35], UserCardType.XL: [0.25, 0.5]}
    USERSTORY_CUSTOMER = {UserCardType.S: [1, 3.5], UserCardType.M: [2.5, 7],
                          UserCardType.L: [5, 14], UserCardType.XL: [10, 28]}
