import os
from neopysqlite.neopysqlite import Pysqlite

# TODO: Pass database filename and tables names via argparse to run tests against a specific database

os.system('sqlite3 test.db < fill_test_db.sql')

test_rows = [
    ('', None),
    ('apple', 'juice'),
    ('lemon', 'lime')
]

current_directory = os.path.dirname(os.path.abspath(__file__))
test_db_path = os.path.join(current_directory, 'test.db')
db = Pysqlite(database_name='Test DB', database_file=test_db_path)


class TestDBAccess:
    def test_db_exists(self):
        assert os.path.isfile(test_db_path), 'Database file does not exist'

    def test_db_accessible(self):
        assert os.access(test_db_path, os.R_OK), 'Database file could not be opened'


class TestDBNotEmpty:
    def test_table_exists(self):
        data = db.get_all_rows(table='sqlite_sequence')
        table_names = [field[0] for field in data]
        assert 'table_one' in table_names, 'Test table "table_one" does not exist'

    def test_db_is_not_empty(self):
        data = db.get_all_rows(table='table_one')
        assert len(data) > 0, 'Test table "table_one" is empty but it should not be empty'


class TestDBContents:
    def test_tables_exist(self):
        test_table_names = [
            'sqlite_sequence',
            'table_one'
        ]
        actual_table_names = db.get_table_names()
        assert test_table_names == actual_table_names, 'Table names retrieved not matching test names'

    def test_row_counts(self):
        data = db.get_all_rows(table='table_one')
        assert len(data) == 5, 'Test row count not as expected'


class TestDBInsert:
    def test_insert_row(self):
        db.insert_row(table='table_one', row_string='(NULL, ?, ?)', row_data=('turkey', 'goose'))
        data = db.get_all_rows('table_one')
        assert data[-1][1] == 'turkey', 'Requested field 1 not as expected'
        assert data[-1][2] == 'goose', 'Requested field 2 not as expected'


class TestDBDelete:
    def test_delete_new_inserted_row(self):
        db.insert_rows(table='table_one', row_string='(NULL, ?, ?)', row_data_list=test_rows)
        db.delete_rows(table='table_one', delete_string='something_not_null = ?', delete_value=('lemon',))
        data = db.get_all_rows(table='table_one')
        assert data[-1][1] == 'apple', 'Inserted field was not properly deleted'

    def test_delete_all_rows(self):
        db.delete_rows(table='table_one')
        data = db.get_all_rows('table_one')
        assert data == [], 'All the table rows were not properly deleted'