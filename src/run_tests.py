import unittest

test_suite = unittest.defaultTestLoader.discover('.')
unittest.TextTestRunner(buffer=True).run(test_suite)
