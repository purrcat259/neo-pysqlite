import sqlite3
import os

version = '0.1.1'


class PysqliteError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class PysqliteCannotAccessError(PysqliteError):
    def __init__(self, db_name):
        self.db_name = db_name

    def __str__(self):
        return 'DB: {} does not exist or could not be accessed'


class Pysqlite:
    def __init__(self, database_name='', database_file=''):
        self.db_name = database_name
        # Check if the database exists and if we can properly access it
        if os.path.isfile(database_file) and os.access(database_file, os.R_OK):
            self.dbcon = sqlite3.connect(database_file)
            self.dbcur = self.dbcon.cursor()
        else:
            raise PysqliteCannotAccessError(db_name=self.db_name)

    def close_connection(self):
        self.dbcon.close()

    def execute_sql(self, execution_string):
        try:
            self.dbcur.execute(execution_string)
        except Exception as e:
            raise PysqliteError('Pysqlite exception: {}'.format(e))

    def get_db_data(self, table):
        try:
            db_data = self.dbcur.execute('SELECT * FROM {}'.format(table))
        except Exception as e:
            raise PysqliteError('Pysqlite experienced the following exception: {}'.format(e))
        data_list = []
        for db_row in db_data:
            data_list.append(db_row)
        if len(data_list) == 0:
            raise PysqliteError('Pysqlite found no data in the table: {} in the DB: {}'.format(table, self.db_name))
        return data_list

    def get_specific_db_data(self, table, filter_string=''):
        try:
            db_data = self.dbcur.execute('SELECT * FROM {} WHERE {}'.format(table, filter_string))
        except Exception as e:
            raise PysqliteError('Pysqlite experienced the following exception: {}'.format(e))
        data_list = []
        for db_row in db_data:
            data_list.append(db_row)
        if len(data_list) == 0:
            raise PysqliteError('Pysqlite found no data in the table: {} in the DB: {} using the filter: {}'.format(
                table,
                self.db_name,
                filter_string
            ))
        return data_list

    def insert_db_data(self, table, row_string, db_data):
        try:
            self.dbcur.execute('INSERT INTO {} VALUES {}'.format(table, row_string), db_data)
            self.dbcon.commit()
        except Exception as e:
            raise PysqliteError('Pysqlite experienced the following exception: {}'.format(e))

    def insert_rows_to_db(self, table, row_string, db_data_list):
        if len(db_data_list) == 0:
            raise PysqliteError('Pysqlite received no data to input')
        if len(db_data_list) == 1:
            self.insert_db_data(table, row_string, db_data_list[0])
        else:
            for data_row in db_data_list:
                try:
                    self.dbcur.execute('INSERT INTO {} VALUES {}'.format(table, row_string), data_row)
                except Exception as e:
                    raise PysqliteError('Pysqlite could not insert a row: {}'.format(e))
                try:
                    self.dbcon.commit()
                except Exception as e:
                    raise PysqliteError('Pysqlite could not commit the data: {}'.format(e))
"""
if __name__ == '__main__':
    ggforcharity_db = Pysqlite('GGforCharity', 'ggforcharity.db')
    data = ggforcharity_db.get_db_data('testing')
    for row in data:
        print(row)
    ggforcharity_db.insert_db_data('testing', '(NULL, ?, ?, ?, ?, ?)', ('Day String', 100, 20, 'Event', 'purrcat259'))
    for row in data:
        print(row)
"""