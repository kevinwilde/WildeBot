import copy
import random
from decimal import *

class Player(object):
    """A basic AI (or human) player."""

    HUMAN = 0
    RANDOM = 1
    MINIMAX = 2
    ABPRUNE = 3
    CUSTOM = 4
    CUSTOM_ALT = 5
    
    def __init__(self, playerNum, playerType, ply=0):
        """Initialize a Player with a playerNum (1 or 2), playerType
        (one of the constants such as HUMAN), and a ply (default is 0).
        """
        self.num = playerNum
        self.opp = 2 - playerNum + 1
        self.type = playerType
        self.ply = ply

    def __repr__(self):
        """Returns a string representation of the Player."""
        return str(self.num)
        
    def minimax_move(self, board, ply):
        """Choose the best minimax move.  Return (score, move)."""
        move = -1
        score = -float('inf')
        turn = self
        for m in board.legal_moves(self.num):
            #for each legal move
            if ply == 0:
                #if we're at ply 0, we need to call our eval function & return
                return (self.score(board), m)
            if board.game_over():
                return (-1, -1)  # Can't make a move, the game is over
            nb = copy.deepcopy(board)
            #make a new board
            nb.make_move(self.num, m)
            #try the move
            opp = Player(self.opp, self.type, self.ply)
            s = opp.min_value(nb, ply-1, turn)
            #and see what the opponent would do next
            if s > score:
                #if the result is better than our best score so far, save that move,score
                move = m
                score = s
        #return the best score and move so far
        return score, move

    def max_value(self, board, ply, turn):
        """Find the minimax value for the next move for this player at
        a given board configuation. Return score.
        """
        if board.game_over():
            return turn.score(board)
        score = -float('inf')
        for m in board.legal_moves(self.num):
            if ply == 0:
                #print "turn.score(board) in max value is: " + str(turn.score(board))
                return turn.score(board)
            # make a new player to play the other side
            opponent = Player(self.opp, self.type, self.ply)
            # Copy the board so that we don't ruin it
            nextBoard = copy.deepcopy(board)
            nextBoard.make_move(self.num, m)
            s = opponent.min_value(nextBoard, ply-1, turn)
            #print "s in max_value is: " + str(s)
            if s > score:
                score = s
        return score
    
    def min_value(self, board, ply, turn):
        """Find the minimax value for the next move for this player at
        a given board configuation. Return score.
        """
        if board.game_over():
            return turn.score(board)
        score = float('inf')
        for m in board.legal_moves(self.num):
            if ply == 0:
                #print "turn.score(board) in min Value is: " + str(turn.score(board))
                return turn.score(board)
            # make a new player to play the other side
            opponent = Player(self.opp, self.type, self.ply)
            # Copy the board so that we don't ruin it
            nextBoard = copy.deepcopy(board)
            nextBoard.make_move(self.num, m)
            s = opponent.max_value(nextBoard, ply-1, turn)
            #print "s in min_value is: " + str(s)
            if s < score:
                score = s
        return score


    # The default player defines a very simple score function
    # You will write the score function in the MancalaPlayer below
    # to improve on this function.
    def score(self, board):
        """ Returns the score for this player given the state of the board """
        if board.has_won(self.num):
            return 100.0
        elif board.has_won(self.opp):
            return 0.0
        else:
            return 50.0


    def alphabeta_move(self, board, ply):
        """Choose a move with alpha beta pruning. Return (score, move).
        """
        move = -1
        score = -float('inf')
        turn = self
        for m in board.legal_moves(self.num):
            #for each legal move
            if ply == 0:
                #if we're at ply 0, we need to call our eval function & return
                return (self.score(board), m)
            if board.game_over():
                return (-1, -1)  # Can't make a move, the game is over
            nb = copy.deepcopy(board)
            #make a new board
            nb.make_move(self.num, m)
            #try the move
            opp = Player(self.opp, self.type, self.ply)
            s = opp.min_value_alphabeta(nb, ply-1, turn, -float('inf'), float('inf'))
            #and see what the opponent would do next
            if s > score:
                #if the result is better than our best score so far, save that move,score
                move = m
                score = s
        #return the best score and move so far
        return score, move

    def max_value_alphabeta(self, board, ply, turn, alpha, beta):
        """Find the minimax value for the next move for this player at
        a given board configuation. Return score.
        """
        if board.game_over():
            return turn.score(board)
        score = -float('inf')
        for m in board.legal_moves(self.num):
            if ply == 0:
                #print "turn.score(board) in max value is: " + str(turn.score(board))
                return turn.score(board)
            # make a new player to play the other side
            opponent = Player(self.opp, self.type, self.ply)
            # Copy the board so that we don't ruin it
            nextBoard = copy.deepcopy(board)
            nextBoard.make_move(self.num, m)
            s = opponent.min_value_alphabeta(nextBoard, ply-1, turn, alpha, beta)
            #print "s in max_value is: " + str(s)
            if s > score:
                score = s
            if score >= beta:
                return score
            alpha = max(alpha, score)
        return score
    
    def min_value_alphabeta(self, board, ply, turn, alpha, beta):
        """Find the minimax value for the next move for this player at
        a given board configuation. Return score.
        """
        if board.game_over():
            return turn.score(board)
        score = float('inf')
        for m in board.legal_moves(self.num):
            if ply == 0:
                #print "turn.score(board) in min Value is: " + str(turn.score(board))
                return turn.score(board)
            # make a new player to play the other side
            opponent = Player(self.opp, self.type, self.ply)
            # Copy the board so that we don't ruin it
            nextBoard = copy.deepcopy(board)
            nextBoard.make_move(self.num, m)
            s = opponent.max_value_alphabeta(nextBoard, ply-1, turn, alpha, beta)
            #print "s in min_value is: " + str(s)
            if s < score:
                score = s
            if score <= alpha:
                return score
            beta = min(beta, score)
        return score

    def choose_move(self, board):
        """ Returns the next move that this player wants to make """
        if self.type == self.HUMAN:
            move = input("Please enter your move:")
            while not board.legal_move(self.num, move):
                print move, "is not valid"
                move = input("Please enter your move:")
            return move
        elif self.type == self.RANDOM:
            move = random.choice(board.legal_moves(self.num))
            print "chose move", move
            return move
        elif self.type == self.MINIMAX:
            val, move = self.minimax_move(board, self.ply)
            print "chose move", move, " with value", val
            return move
        elif self.type == self.ABPRUNE:
            val, move = self.alphabeta_move(board, self.ply)
            print "chose move", move, " with value", val
            return move
        elif self.type == self.CUSTOM:
            customPlayer = kjw731(self.num, self.type, self.ply)
            val, move = customPlayer.custom_move(board, self.ply)
            print "chose move", move, " with value", val
            return move
        elif self.type == self.CUSTOM_ALT:
            customPlayer = kjw731_Alt(self.num, self.type, self.ply)
            val, move = customPlayer.custom_move(board, self.ply)
            print "chose move", move, " with value", val
            return move
        else:
            print "Unknown player type"
            return -1


# Note, you should change the name of this player to be your netid
class kjw731(Player):
    """Defines a player that knows how to evaluate a Mancala gameboard
    intelligently
    """

    def score(self, board):
        """Evaluate the Mancala board for this player."""
        # Reward player for winning the game (more than 24 pebbles in score cup)
        playerWins = 0
        if board.scoreCups[self.num-1] > 24:
            playerWins = 1000
        
        # Reward player for capturing points and limiting opponent's points
        mancalaDiff = board.scoreCups[self.num-1] - board.scoreCups[self.opp-1]
        # Reward player for cups that can reach mancala cup exactly
        exactMancalaCups = 0
        # Punish player for opponent's cups that can reach their mancala cup exactly
        oppExactMancalaCups = 0
        # Rewards player if we have empty cups that can be captured
        canBeCaptured = 0
        indexWhereStonesCanLand = []
        # Punish player if opponent has empty cups that can capture our pebbles
        oppCanBeCaptured = 0
        oppIndexWhereStonesCanLand = []
        # Reward players for having more pebbles on their side
        ourTotalPebbles = 0
        oppTotalPebbles = 0

        myCups = board.get_players_cups(self.num)
        oppCups = board.get_players_cups(self.opp)

        for n in range(board.NCUPS):
            ourTotalPebbles += myCups[n] # total number of pebbles on our side
            oppTotalPebbles += oppCups[n] # total number of pebbles on opponent's side
            indexWhereStonesCanLand.append(n+myCups[n])
            oppIndexWhereStonesCanLand.append(n+oppCups[n])
            if myCups[n] == 0:
                if n in indexWhereStonesCanLand:
                    canBeCaptured += oppCups[board.NCUPS-n-1] # number of opponent's pebbles that can be captured
            elif myCups[n] == board.NCUPS - n:
                exactMancalaCups += 1
            if oppCups[n] == 0:
                if n in oppIndexWhereStonesCanLand:
                    oppCanBeCaptured += myCups[board.NCUPS-n-1] # number of our pebbles that can be captured by our opponent
            elif oppCups[n] == 6-n:
                oppExactMancalaCups += 1

        # Sum playerWins, ourTotalPebbles, oppTotalPebbles, canBeCaptured, oppCanBeCaptured, mancalaDiff, exactMancalaCups, and oppExactMancalaCups
        return playerWins + 10*(ourTotalPebbles - oppTotalPebbles) + 10*canBeCaptured - 30*oppCanBeCaptured + 30*mancalaDiff + 5*exactMancalaCups - 5*oppExactMancalaCups

    def custom_move(self, board, ply):
        """Make move according to alpha-beta search result."""
        return self.alphabeta_move(board, ply)
        
class kjw731_Alt(Player):
    """Alternate class to use against kjw731.
    Use to compare two score functions by playing against each other.
    """

    def score(self, board):
        """Evaluate the Mancala board for this player."""
        # Reward player for winning the game (more than 24 pebbles in score cup)
        playerWins = 0
        if board.scoreCups[self.num-1] > 24:
            playerWins = 1000
        
        # Reward player for capturing points and limiting opponent's points
        mancalaDiff = board.scoreCups[self.num-1] - board.scoreCups[self.opp-1]
        # Punish player for pebbles across from opponent's empty cups
        capturablePebbles = 0
        # Reward player for cups that can reach mancala exactly
        exactMancalaCups = 0
        oppExactMancalaCups = 0
        # Rewards player if empty cup can be captured
        canCapture = 0
        indexWhereStonesCanLand = []

        myCups = board.get_players_cups(self.num)
        oppCups = board.get_players_cups(self.opp)

        for n in range(board.NCUPS):
            indexWhereStonesCanLand.append(n+myCups[n])
            if myCups[n] == 0:
                if n in indexWhereStonesCanLand:
                    canCapture += oppCups[board.NCUPS-n-1]
            elif myCups[n] == board.NCUPS - n:
                exactMancalaCups += 1
            if oppCups[n] == 0:
                capturablePebbles += myCups[board.NCUPS-n-1]
            elif oppCups[n] == 6-n:
                oppExactMancalaCups += 1

        # Sum playerWins, mancalaDiff, emptyCups, capturablePebbles weighted by importance
        return playerWins + 15*canCapture + 2*mancalaDiff + 10*exactMancalaCups - 10*oppExactMancalaCups - 0.25*capturablePebbles

    def custom_move(self, board, ply):
        """Make move according to alpha-beta search result."""
        return self.alphabeta_move(board, ply)
        
