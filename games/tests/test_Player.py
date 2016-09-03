import unittest
from ..Mancala import *
from ..Player import *
from ..TicTacToe import *

class TestPlayer(unittest.TestCase):

    def test_ttt_minimax_players(self):
        p1 = Player(1, Player.MINIMAX, ply=9)
        p2 = Player(2, Player.MINIMAX, ply=9)
        t = TTTBoard()
        # Speed up test by playing some initial moves
        t.make_move(1, 5)
        t.make_move(2, 1)
        t.make_move(1, 2)

        while not t.game_over():
            if t.turn == 1:
                t.make_move(1, p1.choose_move(t))
            else:
                t.make_move(2, p2.choose_move(t))
        
        self.assertTrue(t.game_over())
        # Minimax players should never lose TTT
        self.assertFalse(t.has_won(1))
        self.assertFalse(t.has_won(2))

    def test_ttt_abprune_players(self):
        p1 = Player(1, Player.ABPRUNE, ply=9)
        p2 = Player(2, Player.ABPRUNE, ply=9)
        t = TTTBoard()
        # Speed up test by playing some initial moves
        t.make_move(1, 5)
        t.make_move(2, 1)
        t.make_move(1, 2)

        while not t.game_over():
            if t.turn == 1:
                t.make_move(1, p1.choose_move(t))
            else:
                t.make_move(2, p2.choose_move(t))
        
        self.assertTrue(t.game_over())
        # ABPrune players should never lose TTT
        self.assertFalse(t.has_won(1))
        self.assertFalse(t.has_won(2))
