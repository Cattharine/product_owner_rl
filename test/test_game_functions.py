import sys

sys.path.insert(0, '..')

import unittest
from game.game import ProductOwnerGame
from game.game_constants import GlobalConstants
from game.rooms.devroom.room import OfficeRoom


class TestGameFunctions(unittest.TestCase):
    def setUp(self):
        self.game = ProductOwnerGame()

    def test_availability_on_start(self):
        self.assertTrue(self.game.userstories.statistical_research_available)
        self.assertFalse(self.game.userstories.user_survey_available)

        # не должно выдать ошибку
        self.game.move_backlog_card(0)
        self.game.move_userstory_card(0)

        # до выпуска MVP нельзя купить комнату или робота
        workers_count = self.game.context.available_developers_count  # это число, не массив
        start_money = self.game.context.get_money()
        self.game.buy_room(1)
        self.assertEqual(workers_count, self.game.context.available_developers_count)
        self.assertEqual(start_money, self.game.context.get_money())
        self.game.buy_robot(0)
        self.assertEqual(workers_count, self.game.context.available_developers_count)
        self.assertEqual(start_money, self.game.context.get_money())

        self.assertFalse(self.game.hud.release_available)
        self.assertFalse(self.game.userstories.release_available)
        self.assertFalse(self.game.backlog.can_start_sprint())

    def test_start_game(self):
        # тестируются действия, выполняемые с момента начала игры до первого релиза включительно

        self.buy_statistical_research(self.game.context.get_money(), len(self.game.userstories.stories_list))
        self.move_userstory_card(len(self.game.userstories.stories_list), len(self.game.userstories.release))
        self.press_userstories_release()

        while not self.game.hud.release_available:
            can_move = self.move_backlog_card()
            while can_move:
                can_move = self.move_backlog_card()

            self.start_sprint()

        self.release_product()
    
    def test_buy_robot_dont_throw(self):
        office = self.game.office
        room: OfficeRoom = office.offices[0]
        room.can_buy_robot = True
        self.assertTrue(room.can_buy_robot)
        self.assertEqual(room.get_workers_count(), 2)
        self.game.buy_robot(0)
        self.assertEqual(room.get_workers_count(), 3)

    def buy_statistical_research(self, current_money, us_count):
        self.game.press_statistical_research()

        self.assertEqual(current_money - GlobalConstants.statistical_research_cost, self.game.context.get_money())
        self.assertEqual(us_count + 2, len(self.game.userstories.stories_list))

    def move_userstory_card(self, us_story_count, us_release_count):
        self.game.move_userstory_card(0)

        self.assertEqual(us_story_count - 1, len(self.game.userstories.stories_list))
        self.assertEqual(us_release_count + 1, len(self.game.userstories.release))

    def press_userstories_release(self):
        self.assertTrue(self.game.userstories.release_available)

        self.game.userstories_start_release()
        self.assertGreater(len(self.game.backlog.backlog), 0)
        self.assertEqual(len(self.game.userstories.release), 0)

    def move_backlog_card(self):
        card_index = self.find_available_to_move_backlog_card()
        if card_index is not None:
            backlog_count = len(self.game.backlog.backlog)
            sprint_count = len(self.game.backlog.sprint)

            self.game.move_backlog_card(card_index)

            self.assertEqual(backlog_count - 1, len(self.game.backlog.backlog))
            self.assertEqual(sprint_count + 1, len(self.game.backlog.sprint))
            return True

        return False

    def find_available_to_move_backlog_card(self):
        backlog = self.game.backlog.backlog
        current_hours = self.game.backlog.calculate_hours_sum()
        hours_boundary = self.game.context.available_developers_count * GlobalConstants.developer_hours
        for i in range(len(backlog)):
            card = backlog[i]
            if card.info.hours + current_hours <= hours_boundary:
                return i

    def start_sprint(self):
        self.assertTrue(self.game.backlog.can_start_sprint())

        self.game.backlog_start_sprint()
        self.assertEqual(len(self.game.backlog.sprint), 0)

    def release_product(self):
        self.assertTrue(self.game.hud.release_available)
        is_first_release = self.game.is_first_release

        self.game.hud_release_product()

        if is_first_release:
            self.assertEqual(self.game.context.customers, 25)
            self.assertEqual(self.game.context.get_loyalty(), 4)
            self.assertTrue(self.game.userstories.available)
            self.assertTrue(self.game.userstories.user_survey_available)
            self.assertTrue(self.game.userstories.statistical_research_available)

        self.assertFalse(self.game.is_first_release)
        self.assertFalse(self.game.context.is_new_game)
        self.assertTrue(len(self.game.completed_us) == 0)


if __name__ == "__main__":
    unittest.main()
