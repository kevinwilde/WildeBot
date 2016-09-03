"""
This module provides a super class for games to inherit, allowing games
to load and save their states using Pickle.
"""

import pickle

class Game(object):
    """
    Class that provides utility functions to load and save games
    """

    def save_game(self, filename):
        """
        Given a file name, save the current game to the file using pickle.
        """
        with open(filename, "w") as f:
            p = pickle.Pickler(f)
            p.dump(self)

    @staticmethod
    def load_game(filename):
        """
        Given a file name, load and return the object stored in the file.
        """
        with open(filename, "r") as f:
            u = pickle.Unpickler(f)
            obj = u.load()
        return obj
