import unittest
import os.path


class TestDBAccessible(unittest.TestCase):
    def test_db_exists(self):
        self.assertTrue(os.path.isfile('test.db'))

    def db_accessible(self):
        self.assertTrue(os.access('test.db', os.R_OK))

