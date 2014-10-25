from django.test import TestCase

# Create your tests here.
from board.tasks import GameError, check_move


class CheckMoveTestCase(TestCase):
    def test_check_move_1(self):
        self.assertRaises(GameError, check_move, 0, 0, [], 3)

    def test_check_move_2(self):
        self.assertRaises(GameError, check_move, 10, 0, [(1, 'player', 3, 4)], 13)

    def test_check_move_2a(self):
        try:
            check_move( 10, 1, [(1, 'player', 3, 4)], 13)
        except GameError:
            self.fail("Should not raise GameError")


    def test_check_move_2c(self):
        self.assertRaises(GameError, check_move, 10, 1, [(1, 'player', 3, 4)], 9)



    def test_check_move_3(self):
        self.assertRaises(GameError, check_move, 0, 10, [(1, 'player', 3, 4)], 3)
