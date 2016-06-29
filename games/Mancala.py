import unittest
from random import *
from copy import *
from Game import *
from Player import *

class MancalaBoard(Game):
    def __init__(self):
        """ Initilize a game board for the game of mancala"""
        self.reset()
        
    def reset(self):
        """ Reselt the mancala board for a new game"""
        self.NCUPS = 6       # Cups per side
        self.scoreCups = [0, 0]
        self.P1Cups = [4]*self.NCUPS
        self.P2Cups = [4]*self.NCUPS
        self.turn = 1

    def __str__(self):
        offset = [8 - len(str(self.scoreCups[0])), 9 - len(str(self.scoreCups[1]))]
        ret = "="*offset[0] + " " + str(self.scoreCups[0]) + " You\n" # Player 1 mancala
        
        for i in range(self.NCUPS):
            ret += (str(i+1) + " (" + str(self.P2Cups[i]) + ") | ("
                    + str(self.P1Cups[self.NCUPS-1-i]) + ") " + str(self.NCUPS-i) + "\n")
        
        ret += "Me " + str(self.scoreCups[1]) + " " + "="*offset[1] + "\n"  # Player 2 mancala
        
        return ret

        
    def legalMove( self, playerNum, cup ):
        """ Returns whether or not a given move is legal or not"""
        if playerNum == 1:
            cups = self.P1Cups
        elif playerNum == 2:
            cups = self.P2Cups
        else:
            print playerNum
            raise ValueError("playerNum must be 1 or 2")
        return cup > 0 and cup <= len(cups) and cups[cup-1] > 0

    def legalMoves( self, playerNum ):
        """ Returns a list of legal moves for the given player """
        if playerNum == 1:
            cups = self.P1Cups
        elif playerNum == 2:
            cups = self.P2Cups
        else:
            print playerNum
            raise ValueError("playerNum must be 1 or 2")
        moves = []
        for m in range(len(cups)):
            if cups[m] != 0:
                moves += [m+1]
        return moves


    def makeMove( self, playerNum, cup ):
        if playerNum != self.turn:
            return False
        again = self.makeMoveHelp(playerNum, cup)
        if self.gameOver():
            # clear out the cups
            for i in range(len(self.P1Cups)):
                self.scoreCups[0] += self.P1Cups[i]
                self.P1Cups[i] = 0
            for i in range(len(self.P2Cups)):
                self.scoreCups[1] += self.P2Cups[i]
                self.P2Cups[i] = 0
            self.turn = 0
            return False
        else:
            if not again:
                self.turn = 2 - playerNum + 1
            return again
            
    def makeMoveHelp( self, playerNum, cup ):
        """ Make a move for the given player.
            Returns True if the player gets another turn and False if not.
            Assumes a legal move"""
        if playerNum == 1:
            cups = self.P1Cups
            oppCups = self.P2Cups
        elif playerNum == 2:
            cups = self.P2Cups
            oppCups = self.P1Cups
        else:
            print playerNum
            raise ValueError("playerNum must be 1 or 2")
        initCups = cups
        nstones = cups[cup-1]  # Pick up the stones
        cups[cup-1] = 0        # Now the cup is empty
        cup += 1
        playAgain = False # bug fix - add this line
        while nstones > 0:
            playAgain = False    
            while cup <= len(cups) and nstones > 0:
                cups[cup-1] += 1
                nstones = nstones - 1
                cup += 1
            if nstones == 0:
                break    # If no more stones, exit the loop
            if cups == initCups:   # If we're on our own side
                self.scoreCups[playerNum-1] += 1
                nstones = nstones - 1
                playAgain = True
            # now switch sides and keep going
            tempCups = cups
            cups = oppCups
            oppCups = tempCups
            cup = 1

        # If playAgain is True, then we landed in our Mancala, so this
        # play is over but we get to go again
        if playAgain:
            return True
        
        # Now see if we ended in a blank space on our side
        if cups == initCups and cups[cup-2] == 1:
            self.scoreCups[playerNum-1] += oppCups[(self.NCUPS-cup)+1]
            oppCups[(self.NCUPS-cup)+1] = 0
            #added 2 lines so that when lands on own open cup, captures
            # opposite stones in addition to my own 1
            self.scoreCups[playerNum-1] += 1
            cups[cup-2] = 0
        return False

    def hasWon( self, playerNum ):
        """ Returns whether or not the given player has won """
        if self.gameOver():
            opp = 2 - playerNum + 1
            return self.scoreCups[playerNum-1] > self.scoreCups[opp-1]
        else:
            return False

    def getPlayersCups( self, playerNum ):
        """ Return the cups for the given player """
        if playerNum == 1:
            return self.P1Cups
        elif playerNum == 2:
            return self.P2Cups
        else:
            print playerNum
            raise ValueError("playerNum must be 1 or 2")
        
    def gameOver(self):
        """ Return true if game is over, false otherwise """
        p1done = self.P1Cups == [0] * self.NCUPS
        p2done = self.P2Cups == [0] * self.NCUPS
        return p1done or p2done


#### Unit Tests
class TestMancala(unittest.TestCase):
    def test_legalMoves_fullBoard(self):
        m = MancalaBoard()
        self.assertEqual(m.legalMoves(1), range(1,7))
        self.assertEqual(m.legalMoves(2), range(1,7))

    def test_legalMoves_emptyBoard(self):
        m = MancalaBoard()
        m.P1Cups = [0] * m.NCUPS
        m.P2Cups = [0] * m.NCUPS
        self.assertEqual(m.legalMoves(1), [])
        self.assertEqual(m.legalMoves(2), [])

    def test_gameOver(self):
        m = MancalaBoard()
        m.P1Cups = [0] * m.NCUPS
        m.P2Cups = [0] * m.NCUPS
        self.assertTrue(m.gameOver())

    def test_not_gameOver(self):
        m = MancalaBoard()
        self.assertFalse(m.gameOver())

    def test_makeMove_disallowWrongPlayer(self):
        m = MancalaBoard()
        self.assertFalse(m.makeMove(2, 1))

    def test_makeMove_1(self):
        """Play cup 3 on initial board"""
        m = MancalaBoard()
        m.makeMove(1, 3)
        self.assertEqual(m.P1Cups, [4,4,0,5,5,5])
        self.assertEqual(m.P2Cups, [4,4,4,4,4,4])
        self.assertEqual(m.turn, 1)
        self.assertEqual(m.scoreCups[0], 1)
        self.assertEqual(m.scoreCups[1], 0)
        self.assertEqual(m.legalMoves(1), [1,2,4,5,6])

if __name__ == '__main__':
    unittest.main()
