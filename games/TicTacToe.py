import unittest
from Game import *
from Player import *

class TTTBoard(Game):
    def __init__(self):
        """ Initializes the data members."""
        self.reset()
        
    def reset( self ):
        """ Reset the board for a new game """
        self.SIZE = 3
        self.board = [' ']*(self.SIZE*self.SIZE)
        self.turn = 1
    
    def __str__(self):
        """ Returns a string representation of the board where
            each empty square is indicated with the number of its move"""
        ret = "\n"
        for i in range(len(self.board)):
            if self.board[i] == " ":
                ret += str(i+1)
            else:
                ret += self.board[i]
            if (i+1) % 3 == 0:
                ret += "\n"
            else:
                ret += " "
        ret += "\n"
        return ret

    def legalMove( self, playerNum, move ):
        """Returns true or false, whether the move is legal for the
        player."""
        return move in self.legalMoves(playerNum)

    def legalMoves( self, playerNum ):
        """ Returns the legal moves remianing for the player in question"""
        moves = []
        for m in range(len(self.board)):
            if self.board[m] == ' ':
                moves.append(m+1)
        return moves

    def makeMove( self, playerNum, pos ):
        """ Make a move for player in pos. """
        move = pos - 1
        
        if (move not in range(len(self.board)) 
            or self.board[move] != ' '
            or self.turn != playerNum):

            return False

        if playerNum == 1:
            self.board[move] = 'X'
        elif playerNum == 2:
            self.board[move] = 'O'
        else:
            print playerNum
            raise ValueError("playerNum must be 1 or 2")
        self.turn = 2 - playerNum + 1
        return True
    
    def rowWin( self, c ):
        """ Has the player playing char c won in a row?"""
        for i in range(self.SIZE):
            if self.board[i*self.SIZE:(i+1)*self.SIZE] == [c]*self.SIZE:
                return True
        return False
    
    def colWin( self, c):
        """ Has the player playing char c won in a column?"""
        for i in range(self.SIZE):
            col = []
            for j in range(self.SIZE):
                col += [self.board[j*self.SIZE+i]]
                if col == [c]*self.SIZE:
                    return True
        return False
    
    def diagWin( self, c ):
        """ Has the player playing char c won in a diagonal?"""
        diag = []
        offdiag = []
        for i in range(self.SIZE):
            diag += self.board[i*self.SIZE+i]
            offdiag += self.board[((i+1)*self.SIZE)-1-i]
            if diag == [c]*self.SIZE or offdiag == [c]*self.SIZE:
                return True
        return False
    
    def hasWonPlayer( self, c ):
        """ Has the player playing c won?"""
        return self.rowWin(c) or self.colWin(c) or self.diagWin(c)
    
    def hasWon( self, playerNum ):
        """ Returns who has won: X, O, or None"""
        if playerNum == 1:
            return self.hasWonPlayer( "X" )
        elif playerNum == 2:
            return self.hasWonPlayer( "O" )
        else:
            print playerNum
            raise ValueError("playerNum must be 1 or 2")

    def gameOver(self):
        """ Returns True if the game is over, and false if not"""
        if self.hasWonPlayer("X") or self.hasWonPlayer("O"):
            return True
        else:
            for move in self.board:
                if move == ' ':
                    return False
            return True


#### Unit Tests
class TestTTT(unittest.TestCase):
    def test_legalmoves_emptyboard(self):
        t = TTTBoard()
        self.assertEqual(t.legalMoves(1), range(1,10))
        self.assertEqual(t.legalMoves(2), range(1,10))

    def test_legalmoves_fullboard(self):
        t = TTTBoard()
        for i in range(1,10):
            self.assertTrue(t.makeMove(t.turn, i))
        self.assertEqual(t.legalMoves(1), [])
        self.assertEqual(t.legalMoves(2), [])

    def test_legalmoves_partialboard(self):
        t = TTTBoard()
        self.assertTrue(t.makeMove(1, 1))
        self.assertTrue(t.makeMove(2, 2))
        self.assertTrue(t.makeMove(1, 3))
        self.assertTrue(t.makeMove(2, 7))
        self.assertTrue(t.makeMove(1, 9))
        self.assertEqual(t.legalMoves(1), [4, 5, 6, 8])
        self.assertEqual(t.legalMoves(2), [4, 5, 6, 8])

    def test_disallow_illegal_move(self):
        t = TTTBoard()
        self.assertTrue(t.makeMove(1, 1))
        self.assertFalse(t.makeMove(2, 1))

    def test_disallow_when_wrong_turn(self):
        t = TTTBoard()
        self.assertTrue(t.makeMove(1, 1))
        self.assertFalse(t.makeMove(1, 2))

    def test_row_win(self):
        t = TTTBoard()
        t.makeMove(1, 1)
        t.makeMove(2, 4)
        t.makeMove(1, 2)
        t.makeMove(2, 5)
        t.makeMove(1, 3)
        self.assertTrue(t.gameOver())
        self.assertTrue(t.hasWon(1))

    def test_col_win(self):
        t = TTTBoard()
        t.makeMove(1, 2)
        t.makeMove(2, 1)
        t.makeMove(1, 5)
        t.makeMove(2, 4)
        t.makeMove(1, 3)
        t.makeMove(2, 7)
        self.assertTrue(t.gameOver())
        self.assertTrue(t.hasWon(2))

    def test_diag_win_1(self):
        t = TTTBoard()
        t.makeMove(1, 1)
        t.makeMove(2, 2)
        t.makeMove(1, 5)
        t.makeMove(2, 6)
        t.makeMove(1, 9)
        self.assertTrue(t.gameOver())
        self.assertTrue(t.hasWon(1))

    def test_diag_win_2(self):
        t = TTTBoard()
        t.makeMove(1, 1)
        t.makeMove(2, 3)
        t.makeMove(1, 2)
        t.makeMove(2, 5)
        t.makeMove(1, 9)
        t.makeMove(2, 7)
        self.assertTrue(t.gameOver())
        self.assertTrue(t.hasWon(2))

    def test_cats_game(self):
        t = TTTBoard()
        self.assertTrue(t.makeMove(1, 5))
        self.assertTrue(t.makeMove(2, 1))
        self.assertTrue(t.makeMove(1, 3))
        self.assertTrue(t.makeMove(2, 7))
        self.assertTrue(t.makeMove(1, 4))
        self.assertTrue(t.makeMove(2, 6))
        self.assertTrue(t.makeMove(1, 2))
        self.assertTrue(t.makeMove(2, 8))
        self.assertTrue(t.makeMove(1, 9))
        self.assertTrue(t.gameOver())
        self.assertFalse(t.hasWon(1))
        self.assertFalse(t.hasWon(2))
        

if __name__ == '__main__':
    unittest.main()
