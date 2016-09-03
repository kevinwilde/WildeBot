import unittest

test_suite = unittest.defaultTestLoader.discover('.')
unittest.TextTestRunner().run(test_suite)
