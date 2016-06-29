import pickle

class Game(object):
    """Class that provides utility functions to load and save games
    """

    def saveGame(self, filename):
        """Given a file name, save the current game to the file using pickle."""
        with open(filename, "w") as f:
            p = pickle.Pickler(f)
            p.dump(self)

    def loadGame(filename):
        """Given a file name, load and return the object stored in the file."""
        with open(filename, "r") as f:
            u = pickle.Unpickler(f)
            dObj = u.load()
        return dObj