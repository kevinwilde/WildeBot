import unittest
from .. import *

class TestBayesClassifier(unittest.TestCase):

    def test_positive_statement(self):
        b = BayesClassifier()
        self.assertTrue(b.classify("This is so amazing!! This is great!") > 0)

    def test_negative_statement(self):
        b = BayesClassifier()
        self.assertTrue(b.classify("This is terrible. It is the worst ever.") < 0)