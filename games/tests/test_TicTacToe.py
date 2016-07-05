import unittest
from ..TicTacToe import *

class TestTTT(unittest.TestCase):
    
    def test_legal_moves_emptyboard(self):
        t = TTTBoard()
        self.assertEqual(t.legal_moves(1), range(1,10))
        self.assertEqual(t.legal_moves(2), range(1,10))

    def test_legal_moves_fullboard(self):
        t = TTTBoard()
        for i in range(1,10):
            self.assertTrue(t.make_move(t.turn, i))
        self.assertEqual(t.legal_moves(1), [])
        self.assertEqual(t.legal_moves(2), [])

    def test_legal_moves_partialboard(self):
        t = TTTBoard()
        self.assertTrue(t.make_move(1, 1))
        self.assertTrue(t.make_move(2, 2))
        self.assertTrue(t.make_move(1, 3))
        self.assertTrue(t.make_move(2, 7))
        self.assertTrue(t.make_move(1, 9))
        self.assertEqual(t.legal_moves(1), [4, 5, 6, 8])
        self.assertEqual(t.legal_moves(2), [4, 5, 6, 8])

    def test_disallow_illegal_move(self):
        t = TTTBoard()
        self.assertTrue(t.make_move(1, 1))
        self.assertFalse(t.make_move(2, 1))

    def test_disallow_when_wrong_turn(self):
        t = TTTBoard()
        self.assertTrue(t.make_move(1, 1))
        self.assertFalse(t.make_move(1, 2))

    def test_row__win(self):
        t = TTTBoard()
        t.make_move(1, 1)
        t.make_move(2, 4)
        t.make_move(1, 2)
        t.make_move(2, 5)
        t.make_move(1, 3)
        self.assertTrue(t.game_over())
        self.assertTrue(t.has_won(1))

    def test_col__win(self):
        t = TTTBoard()
        t.make_move(1, 2)
        t.make_move(2, 1)
        t.make_move(1, 5)
        t.make_move(2, 4)
        t.make_move(1, 3)
        t.make_move(2, 7)
        self.assertTrue(t.game_over())
        self.assertTrue(t.has_won(2))

    def test_diag_win_1(self):
        t = TTTBoard()
        t.make_move(1, 1)
        t.make_move(2, 2)
        t.make_move(1, 5)
        t.make_move(2, 6)
        t.make_move(1, 9)
        self.assertTrue(t.game_over())
        self.assertTrue(t.has_won(1))

    def test_diag_win_2(self):
        t = TTTBoard()
        t.make_move(1, 1)
        t.make_move(2, 3)
        t.make_move(1, 2)
        t.make_move(2, 5)
        t.make_move(1, 9)
        t.make_move(2, 7)
        self.assertTrue(t.game_over())
        self.assertTrue(t.has_won(2))

    def test_cats_game(self):
        t = TTTBoard()
        self.assertTrue(t.make_move(1, 5))
        self.assertTrue(t.make_move(2, 1))
        self.assertTrue(t.make_move(1, 3))
        self.assertTrue(t.make_move(2, 7))
        self.assertTrue(t.make_move(1, 4))
        self.assertTrue(t.make_move(2, 6))
        self.assertTrue(t.make_move(1, 2))
        self.assertTrue(t.make_move(2, 8))
        self.assertTrue(t.make_move(1, 9))
        self.assertTrue(t.game_over())
        self.assertFalse(t.has_won(1))
        self.assertFalse(t.has_won(2))
