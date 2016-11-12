import unittest

from test_RetweetDB import test_RetweetDB

# python -m unittest discover -s tests

suite = unittest.makeSuite(test_RetweetDB, 'test')

# Manually Run the Unit Test Runner
runner = unittest.TextTestRunner()
runner.run(suite)
