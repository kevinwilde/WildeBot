from Game import *

class TTTBoard(Game):

    def __init__(self):
        """Initialize the data members."""
        self.reset()
        
    def reset(self):
        """Reset the board for a new game."""
        self.SIZE = 3
        self.board = [' ']*(self.SIZE*self.SIZE)
        self.turn = 1
    
    def __str__(self):
        """Return a string representation of the board where each
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

    def legal_move(self, playerNum, move):
        """Return true or false, whether the move is legal for the
        player.
        """
        return move in self.legal_moves(playerNum)

    def legal_moves(self, playerNum):
        """Return the legal moves remaining for the player in question.
        """
        moves = []
        for m in range(len(self.board)):
            if self.board[m] == ' ':
                moves.append(m+1)
        return moves

    def make_move(self, playerNum, pos):
        """Make a move for player in pos."""
        move = pos - 1
        
        if (move not in range(len(self.board)) 
                or self.board[move] != ' '
                or self.turn != playerNum):
            return False

        if playerNum == 1:
            self.board[move] = 'X'
        elif playerNum == 2:
            self.board[move] = '0'
        else:
            print playerNum
            raise ValueError("playerNum must be 1 or 2")
        self.turn = 2 - playerNum + 1
        return True
    
    def row_win(self, c):
        """Determine if the player playing char c won in a row."""
        for i in range(self.SIZE):
            if self.board[i*self.SIZE:(i+1)*self.SIZE] == [c]*self.SIZE:
                return True
        return False
    
    def col_win(self, c):
        """Determine if the player playing char c won in a column."""
        for i in range(self.SIZE):
            col = []
            for j in range(self.SIZE):
                col += [self.board[j*self.SIZE+i]]
                if col == [c]*self.SIZE:
                    return True
        return False
    
    def diag_win(self, c):
        """Determine if the player playing char c won in a diagonal."""
        diag = []
        offdiag = []
        for i in range(self.SIZE):
            diag += self.board[i*self.SIZE+i]
            offdiag += self.board[((i+1)*self.SIZE)-1-i]
            if diag == [c]*self.SIZE or offdiag == [c]*self.SIZE:
                return True
        return False
    
    def has_won_player(self, c):
        """Determine if the player playing char c has won."""
        return self.row_win(c) or self.col_win(c) or self.diag_win(c)
    
    def has_won(self, playernum):
        """Determine if the player denoted by playernum has won."""
        if playernum == 1:
            return self.has_won_player('X')
        elif playernum == 2:
            return self.has_won_player('0')
        else:
            raise ValueError("playernum must be 1 or 2")

    def board_full(self):
        """Determine if board is full."""
        for square in self.board:
            if square == ' ':
                return False
        return True

    def game_over(self):
        """Determine if game is over."""
        return (self.has_won_player('X') or self.has_won_player('0')
                or self.board_full())
