from pysqlite import Pysqlite
import unittest
import os.path


class TestDBAccessible(unittest.TestCase):
    def test_db_exists(self):
        self.assertTrue(os.path.isfile('test.db'))

    def db_accessible(self):
        self.assertTrue(os.access('test.db', os.R_OK))


class TestDBNotEmpty(unittest.TestCase):
    def test_db_table_exists(self):
        db = Pysqlite(database_name='test db', database_file='test.db')
        data = db.get_db_data('sqlite_sequence')
        table_names = [field[0] for field in data]
        self.assertTrue('table_one' in table_names)

    def test_db_not_empty(self):
        db = Pysqlite(database_name='test db', database_file='test.db')
        data = db.get_db_data('table_one')
        self.assertGreater(len(data), 0)

if __name__ == '__main__':
    unittest.main()
