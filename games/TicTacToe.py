"""
This module provides an interface for two players to play Tic Tac Toe.
"""

from .Game import Game

class TTTBoard(Game):

    def __init__(self):
        self.size = 3
        self.board = [' ']*(self.size*self.size)
        self.turn = 1

    def __str__(self):
        """
        Return a string representation of the board where each
        empty square is indicated with the number of its move.
        """
        ret = "\n"
        for i in range(len(self.board)):
            if self.board[i] == " ":
                ret += str(i+1)
            else:
                ret += self.board[i]

            if (i+1) % 3 == 0:
                if (i+1) != len(self.board):
                    ret += "\n" + "-"*9 + "\n"
            else:
                ret += " | "

        ret += "\n"
        return ret

    def legal_move(self, playernum, move):
        return move in self.legal_moves(playernum)

    def legal_moves(self, playernum):
        moves = []
        for move in range(len(self.board)):
            if self.board[move] == ' ':
                moves.append(move+1)
        return moves

    def make_move(self, playernum, pos):
        move = pos - 1

        if (move not in range(len(self.board))
            or self.board[move] != ' '
            or self.turn != playernum):
            
            return False

        if playernum == 1:
            self.board[move] = 'X'
        elif playernum == 2:
            self.board[move] = '0'
        else:
            print playernum
            raise ValueError("playernum must be 1 or 2")
        self.turn = 2 - playernum + 1
        return True

    def row_win(self, c):
        """Determine if the player playing char c won in a row."""
        for i in range(self.size):
            if self.board[i*self.size:(i+1)*self.size] == [c]*self.size:
                return True
        return False

    def col_win(self, c):
        """Determine if the player playing char c won in a column."""
        for i in range(self.size):
            col = []
            for j in range(self.size):
                col += [self.board[j*self.size+i]]
                if col == [c]*self.size:
                    return True
        return False

    def diag_win(self, c):
        """Determine if the player playing char c won in a diagonal."""
        diag = []
        offdiag = []
        for i in range(self.size):
            diag += self.board[i*self.size+i]
            offdiag += self.board[((i+1)*self.size)-1-i]
            if diag == [c]*self.size or offdiag == [c]*self.size:
                return True
        return False

    def has_won_player(self, c):
        return self.row_win(c) or self.col_win(c) or self.diag_win(c)

    def has_won(self, playernum):
        if playernum == 1:
            return self.has_won_player('X')
        elif playernum == 2:
            return self.has_won_player('0')
        else:
            raise ValueError("playernum must be 1 or 2")

    def board_full(self):
        for square in self.board:
            if square == ' ':
                return False
        return True

    def game_over(self):
        return (self.has_won_player('X') or self.has_won_player('0')
                or self.board_full())
