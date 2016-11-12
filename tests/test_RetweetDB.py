import unittest

import yaml

from classes import RetweetDB


class test_RetweetDB(unittest.TestCase):
    def setUp(self):

        # Specify the file with your DB connection.
        filename = "../jkbbotfactory.yaml"

        try:
            with open(filename, 'r') as f:
                yml = yaml.load(f)
        except IOError:
            print "Error Opening Config File: " + filename
            exit(1)

        self.rtdb = RetweetDB.RetweetDB(
            yml['retweetdb']['odbc_driver'],
            yml['retweetdb']['hostname'],
            yml['retweetdb']['port'],
            yml['retweetdb']['database'],
            yml['retweetdb']['username'],
            yml['retweetdb']['password'],
            yml['retweetdb']['context']
        )

    def tearDown(self):
        self.rtdb.close()

    def test_pass(self):
        """ Just test a Pass """
        self.assertEquals(1, 1)

    def test_isTweetLogged(self):
        """ Test the is_tweet_logged() Function """

        # This long number doesn't exist
        self.assertEquals(self.rtdb.is_tweet_logged("4444444777777444444444444444444447"), False)

        # Insert a Tweet into the table, test for it, then delete it when we're done.
        self.rtdb.log_tweet('4444444777777444444444', 'UnitTest', 'PyUnit')
        self.assertEquals(self.rtdb.is_tweet_logged('4444444777777444444444'), True)
        self.rtdb.delete_tweet('4444444777777444444444')
