from pysqlite import Pysqlite
import unittest
import os.path

# TODO: Pass database filename and tables names via argparse to run tests against a specific database


class TestDBAccessible(unittest.TestCase):
    def test_db_exists(self):
        self.assertTrue(os.path.isfile('test.db'), msg='Database file does not exist')

    def db_accessible(self):
        self.assertTrue(os.access('test.db', os.R_OK), msg='Database file could not be accessed')


class TestDBNotEmpty(unittest.TestCase):
    def test_db_table_exists(self):
        db = Pysqlite(database_name='test db', database_file='test.db')
        data = db.get_db_data('sqlite_sequence')
        table_names = [field[0] for field in data]
        self.assertTrue('table_one' in table_names, msg='Table table_one does not exist')

    def test_db_not_empty(self):
        db = Pysqlite(database_name='test db', database_file='test.db')
        data = db.get_db_data('table_one')
        self.assertGreater(len(data), 0, msg='Test table_one is empty')


class TestDBContents(unittest.TestCase):
    def test_contents_count(self):
        db = Pysqlite(database_name='test db', database_file='test.db')
        data = db.get_db_data('table_one')
        self.assertEqual(len(data), 4, msg='Test contents not as expected')


if __name__ == '__main__':
    unittest.main()
