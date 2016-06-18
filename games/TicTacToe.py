import pickle
from Player import *

class TTTBoard:
    def __init__(self):
        """ Initializes the data members."""
        self.SIZE = 3
        self.board = [' ']*(self.SIZE*self.SIZE)
        self.turn = 1
    
    def __str__(self):
        """ Returns a string representation of the board where
            each empty square is indicated with the number of its move"""
        ret = "\n"
        for i in range(len(self.board)):
            if self.board[i] == " ":
                ret += str(i)
            else:
                ret+=self.board[i]
            if (i+1) % 3 == 0:
                ret+="\n"
            else:
                ret += " "
        ret += "\n"
        return ret

    def legalMove( self, playerNum, move ):
        """Returns true or false, whether the move is legal for the
        player."""
        return move in self.legalMoves(playerNum)

    def legalMoves( self, playerNum ):
        """ Returns the legal moves reminaing for the player in question"""
        moves = []
        for m in range( len(self.board)):
            if self.board[m] == ' ':
                moves += [m]
        return moves

    def makeMove( self, playerNum, pos ):
        """ Make a move for player in pos.  Assumes pos is a legal move. """
        move = pos
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
        
    def reset( self ):
        """ Reset the board for a new game """
        self.board = [' ']*(self.SIZE*self.SIZE)

    def saveGame(self, filename):
        """Given a file name, save the current game to the file using pickle."""
        with open(filename, "w") as f:
            p = pickle.Pickler(f)
            p.dump(self)

    def loadGame(self, filename):
        """Given a file name, load and return the object stored in the file."""
        with open(filename, "r") as f:
            u = pickle.Unpickler(f)
            dObj = u.load()
        return dObj