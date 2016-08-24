"""
This module provides an interface for two players to play Mancala.
"""

from .Game import Game

class MancalaBoard(Game):

    def __init__(self):
        """Initialize a game board for the game of mancala."""
        self.num_cups = 6
        self.score_cups = [0, 0]
        self.P1Cups = [4]*self.num_cups
        self.P2Cups = [4]*self.num_cups
        self.turn = 1

    def __str__(self):
        offset = [8 - len(str(self.score_cups[0])), 9 - len(str(self.score_cups[1]))]

        # Player 1 mancala
        ret = "="*offset[0] + " " + str(self.score_cups[0]) + " You\n"

        for i in range(self.num_cups):
            ret += (str(i+1) + " (" + str(self.P2Cups[i]) + ") | ("
                    + str(self.P1Cups[self.num_cups-1-i]) + ") " + str(self.num_cups-i) + "\n")

        # Player 2 mancala
        ret += "Me " + str(self.score_cups[1]) + " " + "="*offset[1] + "\n"

        return ret

    def legal_move(self, playernum, move):
        """Return whether or not a given move is legal."""
        return move in self.legal_moves(playernum)

    def legal_moves(self, playernum):
        """Return a list of legal moves for the given player."""
        cups = self.get_players_cups(playernum)
        moves = []
        for move in range(len(cups)):
            if cups[move] != 0:
                moves.append(move+1)
        return moves

    def make_move(self, playernum, cup):
        """ Make a move for the given player.
        Return True if the player gets another turn and False if not.
        Assumes a legal move.
        """
        if playernum != self.turn:
            return False
        again = self.make_move_help(playernum, cup)
        if self.game_over():
            # Clear out the cups
            for i in range(len(self.P1Cups)):
                self.score_cups[0] += self.P1Cups[i]
                self.P1Cups[i] = 0
            for i in range(len(self.P2Cups)):
                self.score_cups[1] += self.P2Cups[i]
                self.P2Cups[i] = 0
            self.turn = 0
            return False
        else:
            if not again:
                self.turn = 2 - playernum + 1
            return again

    def make_move_help(self, playernum, cup):
        """Helper for make_move."""
        if playernum == 1:
            cups = self.P1Cups
            opp_cups = self.P2Cups
        elif playernum == 2:
            cups = self.P2Cups
            opp_cups = self.P1Cups
        else:
            print playernum
            raise ValueError("playernum must be 1 or 2")
        init_cups = cups
        nstones = cups[cup-1]  # Pick up the stones
        cups[cup-1] = 0        # Now the cup is empty
        cup += 1
        play_again = False # bug fix - add this line
        while nstones > 0:
            play_again = False
            while cup <= len(cups) and nstones > 0:
                cups[cup-1] += 1
                nstones = nstones - 1
                cup += 1
            if nstones == 0:
                break    # If no more stones, exit the loop
            if cups == init_cups:   # If we're on our own side
                self.score_cups[playernum-1] += 1
                nstones = nstones - 1
                play_again = True
            # now switch sides and keep going
            temp_cups = cups
            cups = opp_cups
            opp_cups = temp_cups
            cup = 1

        # If play_again is True, then we landed in our Mancala, so this
        # play is over but we get to go again
        if play_again:
            return True

        # Now see if we ended in a blank space on our side
        if cups == init_cups and cups[cup-2] == 1:
            self.score_cups[playernum-1] += opp_cups[(self.num_cups-cup)+1]
            opp_cups[(self.num_cups-cup)+1] = 0
            #added 2 lines so that when lands on own open cup, captures
            # opposite stones in addition to my own 1
            self.score_cups[playernum-1] += 1
            cups[cup-2] = 0
        return False

    def has_won(self, playernum):
        """Determine if given player has won."""
        if self.game_over():
            opp = 2 - playernum + 1
            return self.score_cups[playernum-1] > self.score_cups[opp-1]
        else:
            return False

    def get_players_cups(self, playernum):
        """Return the cups for the given player."""
        if playernum == 1:
            return self.P1Cups
        elif playernum == 2:
            return self.P2Cups
        else:
            raise ValueError("playernum must be 1 or 2")

    def game_over(self):
        """Determine if game is over."""
        p1done = self.P1Cups == [0] * self.num_cups
        p2done = self.P2Cups == [0] * self.num_cups
        return p1done or p2done
