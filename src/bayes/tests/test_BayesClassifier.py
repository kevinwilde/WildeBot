import unittest
from .. import *

class TestBayesClassifier(unittest.TestCase):

    def setUp(self):
        self.bc = BayesClassifier()

    def test_positive_statement(self):
        self.assertTrue(self.bc.classify("This is so amazing!! This is great!") > 0)

    def test_negative_statement(self):
        self.assertTrue(self.bc.classify("This is terrible. It is the worst ever.") < 0)