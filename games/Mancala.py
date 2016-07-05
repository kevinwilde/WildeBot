from Game import Game

class MancalaBoard(Game):

    def __init__(self):
        """Initialize a game board for the game of mancala."""
        self.reset()
        
    def reset(self):
        """Reset the mancala board for a new game."""
        self.NCUPS = 6
        self.scoreCups = [0, 0]
        self.P1Cups = [4]*self.NCUPS
        self.P2Cups = [4]*self.NCUPS
        self.turn = 1

    def __str__(self):
        offset = [8 - len(str(self.scoreCups[0])), 9 - len(str(self.scoreCups[1]))]
        
        # Player 1 mancala
        ret = "="*offset[0] + " " + str(self.scoreCups[0]) + " You\n"
        
        for i in range(self.NCUPS):
            ret += (str(i+1) + " (" + str(self.P2Cups[i]) + ") | ("
                    + str(self.P1Cups[self.NCUPS-1-i]) + ") " + str(self.NCUPS-i) + "\n")
        
        # Player 2 mancala
        ret += "Me " + str(self.scoreCups[1]) + " " + "="*offset[1] + "\n"        
        
        return ret

        
    def legal_move(self, playernum, cup):
        """Return whether or not a given move is legal."""
        cups = self.get_players_cups(playernum)
        return cup > 0 and cup <= len(cups) and cups[cup-1] > 0

    def legal_moves(self, playernum):
        """Return a list of legal moves for the given player."""
        cups = self.get_players_cups(playernum)
        moves = []
        for m in range(len(cups)):
            if cups[m] != 0:
                moves += [m+1]
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
                self.scoreCups[0] += self.P1Cups[i]
                self.P1Cups[i] = 0
            for i in range(len(self.P2Cups)):
                self.scoreCups[1] += self.P2Cups[i]
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
            oppCups = self.P2Cups
        elif playernum == 2:
            cups = self.P2Cups
            oppCups = self.P1Cups
        else:
            print playernum
            raise ValueError("playernum must be 1 or 2")
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
                self.scoreCups[playernum-1] += 1
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
            self.scoreCups[playernum-1] += oppCups[(self.NCUPS-cup)+1]
            oppCups[(self.NCUPS-cup)+1] = 0
            #added 2 lines so that when lands on own open cup, captures
            # opposite stones in addition to my own 1
            self.scoreCups[playernum-1] += 1
            cups[cup-2] = 0
        return False

    def has_won(self, playernum):
        """Determine if given player has won."""
        if self.game_over():
            opp = 2 - playernum + 1
            return self.scoreCups[playernum-1] > self.scoreCups[opp-1]
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
        p1done = self.P1Cups == [0] * self.NCUPS
        p2done = self.P2Cups == [0] * self.NCUPS
        return p1done or p2done
