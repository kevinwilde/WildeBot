"""
This module holds a class for a basic AI (or human) player.
"""

import copy
import random

class Player(object):
    """A basic AI (or human) player."""

    HUMAN = 0
    RANDOM = 1
    MINIMAX = 2
    ABPRUNE = 3
    CUSTOM = 4

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
        best_move = -1
        best_score = -float('inf')
        turn = self
        for move in board.legal_moves(self.num):
            #for each legal move
            if ply == 0:
                #if we're at ply 0, we need to call our eval function & return
                return (self.score(board), move)
            if board.game_over():
                return (-1, -1)  # Can't make a move, the game is over
            #make a new board
            new_board = copy.deepcopy(board)
            #try the move
            new_board.make_move(self.num, move)
            opp = Player(self.opp, self.type, self.ply)
            score = opp.min_value(new_board, ply-1, turn)
            #and see what the opponent would do next
            if score > best_score:
                #if the result is better than our best score so far,
                # save that move, score
                best_move = move
                best_score = score
        #return the best score and move so far
        return best_score, best_move

    def max_value(self, board, ply, turn):
        """Find the minimax value for the next move for this player at
        a given board configuation. Return score.
        """
        if board.game_over():
            return turn.score(board)
        best_score = -float('inf')
        for move in board.legal_moves(self.num):
            if ply == 0:
                return turn.score(board)
            # make a new player to play the other side
            opponent = Player(self.opp, self.type, self.ply)
            new_board = copy.deepcopy(board)
            new_board.make_move(self.num, move)
            score = opponent.min_value(new_board, ply-1, turn)
            if score > best_score:
                best_score = score
        return best_score

    def min_value(self, board, ply, turn):
        """Find the minimax value for the next move for this player at
        a given board configuation. Return score.
        """
        if board.game_over():
            return turn.score(board)
        best_score = float('inf')
        for move in board.legal_moves(self.num):
            if ply == 0:
                return turn.score(board)
            # make a new player to play the other side
            opponent = Player(self.opp, self.type, self.ply)
            new_board = copy.deepcopy(board)
            new_board.make_move(self.num, move)
            score = opponent.max_value(new_board, ply-1, turn)
            if score < best_score:
                best_score = score
        return best_score


    # The default player defines a very simple score function
    def score(self, board):
        """Return the score for this player given the state of the board."""
        if board.has_won(self.num):
            return 100.0
        elif board.has_won(self.opp):
            return 0.0
        else:
            return 50.0

    def alphabeta_move(self, board, ply):
        """Choose a move with alpha beta pruning. Return (score, move).
        """
        best_move = -1
        best_score = -float('inf')
        turn = self
        for move in board.legal_moves(self.num):
            #for each legal move
            if ply == 0:
                #if we're at ply 0, we need to call our eval function & return
                return (self.score(board), move)
            if board.game_over():
                return (-1, -1)  # Can't make a move, the game is over
            #make a new board
            new_board = copy.deepcopy(board)
            #try the move
            new_board.make_move(self.num, move)
            opp = Player(self.opp, self.type, self.ply)
            score = opp.min_value_alphabeta(new_board, ply-1, turn, -float('inf'), float('inf'))
            #and see what the opponent would do next
            if score > best_score:
                #if the result is better than our best score so far, save that move,score
                best_move = move
                best_score = score
        #return the best score and move so far
        return best_score, best_move

    def max_value_alphabeta(self, board, ply, turn, alpha, beta):
        """Find the minimax value for the next move for this player at
        a given board configuation. Return score.
        """
        if board.game_over():
            return turn.score(board)
        best_score = -float('inf')
        for move in board.legal_moves(self.num):
            if ply == 0:
                return turn.score(board)
            # make a new player to play the other side
            opponent = Player(self.opp, self.type, self.ply)
            new_board = copy.deepcopy(board)
            new_board.make_move(self.num, move)
            score = opponent.min_value_alphabeta(new_board, ply-1, turn, alpha, beta)
            if score > best_score:
                best_score = score
            if best_score >= beta:
                return best_score
            alpha = max(alpha, best_score)
        return best_score

    def min_value_alphabeta(self, board, ply, turn, alpha, beta):
        """Find the minimax value for the next move for this player at
        a given board configuation. Return score.
        """
        if board.game_over():
            return turn.score(board)
        best_score = float('inf')
        for move in board.legal_moves(self.num):
            if ply == 0:
                return turn.score(board)
            # make a new player to play the other side
            opponent = Player(self.opp, self.type, self.ply)
            new_board = copy.deepcopy(board)
            new_board.make_move(self.num, move)
            score = opponent.max_value_alphabeta(new_board, ply-1, turn, alpha, beta)
            if score < best_score:
                best_score = score
            if best_score <= alpha:
                return best_score
            beta = min(beta, best_score)
        return best_score

    def choose_move(self, board):
        """ Returns the next move that this player wants to make """
        if self.type == self.HUMAN:
            move = int(raw_input("Please enter your move:"))
            while not board.legal_move(self.num, move):
                print move, "is not valid"
                move = int(raw_input("Please enter your move:"))
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
            player = CustomPlayer(self.num, self.type, self.ply)
            val, move = player.custom_move(board, self.ply)
            print "chose move", move, " with value", val
            return move
        else:
            print "Unknown player type"
            return -1


class CustomPlayer(Player):
    """Defines a player that knows how to evaluate a Mancala gameboard
    intelligently
    """

    def score(self, board):
        """Evaluate the Mancala board for this player."""
        # Reward player for winning the game (more than 24 pebbles in score cup)
        player_wins = 0
        if board.score_cups[self.num-1] > 24:
            player_wins = 1000

        # Reward player for capturing points and limiting opponent's points
        mancala_diff = board.score_cups[self.num-1] - board.score_cups[self.opp-1]
        # Reward player for cups that can reach mancala cup exactly
        exact_mancala_cups = 0
        # Punish player for opponent's cups that can reach their mancala exactly
        opp_exact_mancala_cups = 0
        # Rewards player if we have empty cups that can be captured
        can_be_captured = 0
        index_where_stones_can_land = []
        # Punish player if opponent has empty cups that can capture our pebbles
        opp_can_be_captured = 0
        opp_index_where_stones_can_land = []
        # Reward players for having more pebbles on their side
        our_total_pebbles = 0
        opp_total_pebbles = 0

        my_cups = board.get_players_cups(self.num)
        opp_cups = board.get_players_cups(self.opp)

        for i in range(board.num_cups):
            # total number of pebbles on our side
            our_total_pebbles += my_cups[i]
            # total number of pebbles on opponent's side
            opp_total_pebbles += opp_cups[i]
            index_where_stones_can_land.append(i+my_cups[i])
            opp_index_where_stones_can_land.append(i+opp_cups[i])
            if my_cups[i] == 0:
                if i in index_where_stones_can_land:
                    # number of opponent's pebbles that can be captured
                    can_be_captured += opp_cups[board.num_cups-i-1]
            elif my_cups[i] == board.num_cups - i:
                exact_mancala_cups += 1
            if opp_cups[i] == 0:
                if i in opp_index_where_stones_can_land:
                    # number of our pebbles that can be captured by our opponent
                    opp_can_be_captured += my_cups[board.num_cups-i-1]
            elif opp_cups[i] == 6-i:
                opp_exact_mancala_cups += 1

        return (player_wins
                + 10*(our_total_pebbles - opp_total_pebbles)
                + 10*can_be_captured
                - 30*opp_can_be_captured
                + 30*mancala_diff
                + 5*exact_mancala_cups
                - 5*opp_exact_mancala_cups)

    def custom_move(self, board, ply):
        """Make move according to alpha-beta search result."""
        return self.alphabeta_move(board, ply)
