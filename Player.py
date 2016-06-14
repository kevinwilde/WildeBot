# File: Player.py
# Author(s) names AND netid's: Kevin Cheng (klc954) and Kevin Wilde (kjw731)
# Date: April 22, 2016
# Group work statement: All group members were
#      present and contributing during all work on this project.
# Defines a simple artificially intelligent player agent
# You will define the alpha-beta pruning search algorithm
# You will also define the score function in the MancalaPlayer class,
# a subclass of the Player class.


from random import *
from decimal import *
from copy import *
from MancalaBoard import *

# a constant
INFINITY = 1.0e400

class Player:
    """ A basic AI (or human) player """
    HUMAN = 0
    RANDOM = 1
    MINIMAX = 2
    ABPRUNE = 3
    CUSTOM = 4
    CUSTOM_ALT = 5
    
    def __init__(self, playerNum, playerType, ply=0):
        """Initialize a Player with a playerNum (1 or 2), playerType (one of
        the constants such as HUMAN), and a ply (default is 0)."""
        self.num = playerNum
        self.opp = 2 - playerNum + 1
        self.type = playerType
        self.ply = ply

    def __repr__(self):
        """Returns a string representation of the Player."""
        return str(self.num)
        
    def minimaxMove(self, board, ply):
        """ Choose the best minimax move.  Returns (score, move) """
        move = -1
        score = -INFINITY
        turn = self
        for m in board.legalMoves(self):
            #for each legal move
            if ply == 0:
                #if we're at ply 0, we need to call our eval function & return
                return (self.score(board), m)
            if board.gameOver():
                return (-1, -1)  # Can't make a move, the game is over
            nb = deepcopy(board)
            #make a new board
            nb.makeMove(self, m)
            #try the move
            opp = Player(self.opp, self.type, self.ply)
            s = opp.minValue(nb, ply-1, turn)
            #and see what the opponent would do next
            if s > score:
                #if the result is better than our best score so far, save that move,score
                move = m
                score = s
        #return the best score and move so far
        return score, move

    def maxValue(self, board, ply, turn):
        """ Find the minimax value for the next move for this player
        at a given board configuation. Returns score."""
        if board.gameOver():
            return turn.score(board)
        score = -INFINITY
        for m in board.legalMoves(self):
            if ply == 0:
                #print "turn.score(board) in max value is: " + str(turn.score(board))
                return turn.score(board)
            # make a new player to play the other side
            opponent = Player(self.opp, self.type, self.ply)
            # Copy the board so that we don't ruin it
            nextBoard = deepcopy(board)
            nextBoard.makeMove(self, m)
            s = opponent.minValue(nextBoard, ply-1, turn)
            #print "s in maxValue is: " + str(s)
            if s > score:
                score = s
        return score
    
    def minValue(self, board, ply, turn):
        """ Find the minimax value for the next move for this player
            at a given board configuation. Returns score."""
        if board.gameOver():
            return turn.score(board)
        score = INFINITY
        for m in board.legalMoves(self):
            if ply == 0:
                #print "turn.score(board) in min Value is: " + str(turn.score(board))
                return turn.score(board)
            # make a new player to play the other side
            opponent = Player(self.opp, self.type, self.ply)
            # Copy the board so that we don't ruin it
            nextBoard = deepcopy(board)
            nextBoard.makeMove(self, m)
            s = opponent.maxValue(nextBoard, ply-1, turn)
            #print "s in minValue is: " + str(s)
            if s < score:
                score = s
        return score


    # The default player defines a very simple score function
    # You will write the score function in the MancalaPlayer below
    # to improve on this function.
    def score(self, board):
        """ Returns the score for this player given the state of the board """
        if board.hasWon(self.num):
            return 100.0
        elif board.hasWon(self.opp):
            return 0.0
        else:
            return 50.0

    # You should not modify anything before this point.
    # The code you will add to this file appears below this line.

    # You will write this function (and any helpers you need)
    # You should write the function here in its simplest form:
    #   1. Use ply to determine when to stop (when ply == 0)
    #   2. Search the moves in the order they are returned from the board's
    #       legalMoves function.
    # However, for your custom player, you may copy this function
    # and modify it so that it uses a different termination condition
    # and/or a different move search order.
    def alphaBetaMove(self, board, ply):
        """ Choose a move with alpha beta pruning.  Returns (score, move) """
        """ Choose the best minimax move.  Returns (score, move) """
        move = -1
        score = -INFINITY
        turn = self
        for m in board.legalMoves(self):
            #for each legal move
            if ply == 0:
                #if we're at ply 0, we need to call our eval function & return
                return (self.score(board), m)
            if board.gameOver():
                return (-1, -1)  # Can't make a move, the game is over
            nb = deepcopy(board)
            #make a new board
            nb.makeMove(self, m)
            #try the move
            opp = Player(self.opp, self.type, self.ply)
            s = opp.minValueAlphaBeta(nb, ply-1, turn, -INFINITY, INFINITY)
            #and see what the opponent would do next
            if s > score:
                #if the result is better than our best score so far, save that move,score
                move = m
                score = s
        #return the best score and move so far
        return score, move

    def maxValueAlphaBeta(self, board, ply, turn, alpha, beta):
        """ Find the minimax value for the next move for this player
        at a given board configuation. Returns score."""
        if board.gameOver():
            return turn.score(board)
        score = -INFINITY
        for m in board.legalMoves(self):
            if ply == 0:
                #print "turn.score(board) in max value is: " + str(turn.score(board))
                return turn.score(board)
            # make a new player to play the other side
            opponent = Player(self.opp, self.type, self.ply)
            # Copy the board so that we don't ruin it
            nextBoard = deepcopy(board)
            nextBoard.makeMove(self, m)
            s = opponent.minValueAlphaBeta(nextBoard, ply-1, turn, alpha, beta)
            #print "s in maxValue is: " + str(s)
            if s > score:
                score = s
            if score >= beta:
                return score
            alpha = max(alpha, score)
        return score
    
    def minValueAlphaBeta(self, board, ply, turn, alpha, beta):
        """ Find the minimax value for the next move for this player
            at a given board configuation. Returns score."""
        if board.gameOver():
            return turn.score(board)
        score = INFINITY
        for m in board.legalMoves(self):
            if ply == 0:
                #print "turn.score(board) in min Value is: " + str(turn.score(board))
                return turn.score(board)
            # make a new player to play the other side
            opponent = Player(self.opp, self.type, self.ply)
            # Copy the board so that we don't ruin it
            nextBoard = deepcopy(board)
            nextBoard.makeMove(self, m)
            s = opponent.maxValueAlphaBeta(nextBoard, ply-1, turn, alpha, beta)
            #print "s in minValue is: " + str(s)
            if s < score:
                score = s
            if score <= alpha:
                return score
            beta = min(beta, score)
        return score

    def chooseMove(self, board):
        """ Returns the next move that this player wants to make """
        if self.type == self.HUMAN:
            move = input("Please enter your move:")
            while not board.legalMove(self, move):
                print move, "is not valid"
                move = input( "Please enter your move" )
            return move
        elif self.type == self.RANDOM:
            move = choice(board.legalMoves(self))
            print "chose move", move
            return move
        elif self.type == self.MINIMAX:
            val, move = self.minimaxMove(board, self.ply)
            print "chose move", move, " with value", val
            return move
        elif self.type == self.ABPRUNE:
            val, move = self.alphaBetaMove(board, self.ply)
            print "chose move", move, " with value", val
            return move
        elif self.type == self.CUSTOM:
            # TODO: Implement a custom player
            # You should fill this in with a call to your best move choosing
            # function.  You may use whatever search algorithm and scoring
            # algorithm you like.  Remember that your player must make
            # each move in about 10 seconds or less.
            plyFor10Sec = 9
            customPlayer = kjw731(self.num, self.type, plyFor10Sec)
            val, move = customPlayer.customMove(board, customPlayer.ply)
            print "chose move", move, " with value", val
            return move
        elif self.type == self.CUSTOM_ALT:
            plyFor10Sec = 9
            customPlayer = kjw731_Alt(self.num, self.type, plyFor10Sec)
            val, move = customPlayer.customMove(board, customPlayer.ply)
            print "chose move", move, " with value", val
            return move
        else:
            print "Unknown player type"
            return -1


# Note, you should change the name of this player to be your netid
class kjw731(Player):
    """ Defines a player that knows how to evaluate a Mancala gameboard
        intelligently """

    def score(self, board):
        """ Evaluate the Mancala board for this player """
        # Currently this function just calls Player's score
        # function.  You should replace the line below with your own code
        # for evaluating the board
        # print "Calling score in kjw731"

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

        myCups = board.getPlayersCups(self.num)
        oppCups = board.getPlayersCups(self.opp)

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

    def customMove(self, board, ply):
        """ Make move according to alpha-beta search result """
        # print "Calling customMove with ply =", ply
        return self.alphaBetaMove(board, ply)
        
class kjw731_Alt(Player):
    """ Alternate class to use against kjw731
        Use to compare two score functions by playing against each other
     """

    def score(self, board):
        """ Evaluate the Mancala board for this player """
        # Currently this function just calls Player's score
        # function.  You should replace the line below with your own code
        # for evaluating the board
        # print "Calling score in kjw731_Alt"

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

        myCups = board.getPlayersCups(self.num)
        oppCups = board.getPlayersCups(self.opp)

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

    def customMove(self, board, ply):
        """ Make move according to alpha-beta search result """
        # print "Calling customMove ALT with ply =", ply
        return self.alphaBetaMove(board, ply)
        
