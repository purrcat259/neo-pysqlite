from pysqlite import Pysqlite
import unittest
import os.path

# TODO: Pass database filename and tables names via argparse to run tests against a specific database

# set the DB as global to avoid initialising it each time
db = Pysqlite(database_name='test db', database_file='test.db')


class TestDBAccessible(unittest.TestCase):
    def test_db_exists(self):
        self.assertTrue(os.path.isfile('test.db'), msg='Database file does not exist')

    def db_accessible(self):
        self.assertTrue(os.access('test.db', os.R_OK), msg='Database file could not be accessed')


class TestDBNotEmpty(unittest.TestCase):
    def test_db_table_exists(self):
        # db = Pysqlite(database_name='test db', database_file='test.db')
        global db
        data = db.get_db_data('sqlite_sequence')
        table_names = [field[0] for field in data]
        self.assertTrue('table_one' in table_names, msg='Table table_one does not exist')

    def test_db_not_empty(self):
        # db = Pysqlite(database_name='test db', database_file='test.db')
        global db
        data = db.get_db_data('table_one')
        self.assertGreater(len(data), 0, msg='Test table_one is empty')


class TestDBContents(unittest.TestCase):
    def test_tables_exist(self):
        global db
        test_table_names = ['table_one', 'sqlite_sequence']
        table_names = db.get_table_names()
        self.assertEqual(table_names, test_table_names, msg='Tables returned: {} not as expected: {}'.format(
            table_names, test_table_names))

    """
    def test_contents_count(self):
        # db = Pysqlite(database_name='test db', database_file='test.db')
        global db
        data = db.get_db_data('table_one')
        self.assertEqual(len(data), 4, msg='Test contents not as expected')
    """

    def test_insert_correct_row(self):
        global db
        db.insert_db_data('table_one', '(NULL, ?, ?)', ('lemon', 'lime'))
        data = db.get_db_data('table_one')
        self.assertTrue(data[-1][1] == 'lemon', msg='Retrieved field 1 does not match given field 1')
        self.assertTrue(data[-1][2] == 'lime', msg='Retrieved field 2 does not match given field 2')


if __name__ == '__main__':
    unittest.main()
