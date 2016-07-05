import unittest
from ..Mancala import *

class TestMancala(unittest.TestCase):

    def test_legal_moves_full_board(self):
        m = MancalaBoard()
        self.assertEqual(m.legal_moves(1), range(1,7))
        self.assertEqual(m.legal_moves(2), range(1,7))

    def test_legal_moves_empty_board(self):
        m = MancalaBoard()
        m.P1Cups = [0] * m.NCUPS
        m.P2Cups = [0] * m.NCUPS
        self.assertEqual(m.legal_moves(1), [])
        self.assertEqual(m.legal_moves(2), [])

    def test_game_over(self):
        m = MancalaBoard()
        m.P1Cups = [0] * m.NCUPS
        m.P2Cups = [0] * m.NCUPS
        self.assertTrue(m.game_over())

    def test_not_game_over(self):
        m = MancalaBoard()
        self.assertFalse(m.game_over())

    def test_make_move_disallow_wrong_player(self):
        m = MancalaBoard()
        self.assertFalse(m.make_move(2, 1))

    def test_make_move_1(self):
        """Play cup 3 on initial board"""
        m = MancalaBoard()
        m.make_move(1, 3)
        self.assertEqual(m.P1Cups, [4,4,0,5,5,5])
        self.assertEqual(m.P2Cups, [4,4,4,4,4,4])
        self.assertEqual(m.turn, 1)
        self.assertEqual(m.scoreCups[0], 1)
        self.assertEqual(m.scoreCups[1], 0)
        self.assertEqual(m.legal_moves(1), [1,2,4,5,6])

    def test_clear_board_at_end(self):
        m = MancalaBoard()
        m.P1Cups = [0,0,0,0,0,1]
        m.scoreCups = [23, 0]
        m.make_move(1, 6)
        self.assertEqual(m.P1Cups, [0] * m.NCUPS)
        self.assertEqual(m.P2Cups, [0] * m.NCUPS)
        self.assertTrue(m.game_over())

    def test_series_of_moves(self):
        m = MancalaBoard()
        again = m.make_move(1, 3)
        self.assertTrue(again)
        again = m.make_move(1, 4)
        self.assertFalse(again)
        self.assertEqual(m.turn, 2)
        again = m.make_move(2, 3)
        self.assertTrue(again)
        again = m.make_move(2, 2)
        self.assertTrue(again)
        again = m.make_move(2, 1)
        self.assertFalse(again)
        self.assertEqual(m.turn, 1)
