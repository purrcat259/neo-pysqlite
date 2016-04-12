import sqlite3
import os

version = '0.1.2'


class PysqliteException(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class PysqliteCannotAccessException(PysqliteException):
    def __init__(self, db_name):
        self.db_name = db_name

    def __str__(self):
        return 'DB: {} does not exist or could not be accessed'


class Pysqlite:
    # Initialise the class, make sure the file is accessible and open a connection
    def __init__(self, database_name='', database_file='', verbose=False):
        self.db_name = database_name
        self.verbose = verbose
        if self.verbose:
            print('Pysqlite object initialising')
        # Check if the database exists and if we can properly access it
        if os.path.isfile(database_file) and os.access(database_file, os.R_OK):
            self.dbcon = sqlite3.connect(database_file)
            self.dbcur = self.dbcon.cursor()
            if self.verbose:
                print('Pysqlite successfully opened database connection to: {}'.format(self.db_name))
        else:
            raise PysqliteCannotAccessException(db_name=self.db_name)

    # closes the current connection
    def close_connection(self):
        self.dbcon.close()

    # takes a string of SQL to execute, beware using this without validation
    def execute_sql(self, execution_string):
        try:
            self.dbcur.execute(execution_string)
        except Exception as e:
            raise PysqliteException('Pysqlite exception: {}'.format(e))

    # get all the data in a table as a list
    def get_db_data(self, table):
        try:
            db_data = self.dbcur.execute('SELECT * FROM {}'.format(table))
        except Exception as e:
            raise PysqliteException('Pysqlite experienced the following exception: {}'.format(e))
        data_list = []
        for db_row in db_data:
            data_list.append(db_row)
        return data_list

    # get data from a table whilst passing an SQL filter condition
    def get_specific_db_data(self, table, filter_string=''):
        try:
            db_data = self.dbcur.execute('SELECT * FROM {} WHERE {}'.format(table, filter_string))
        except Exception as e:
            raise PysqliteException('Pysqlite experienced the following exception: {}'.format(e))
        data_list = []
        for db_row in db_data:
            data_list.append(db_row)
        return data_list

    # insert a row to a table, pass the schema of the row as the row_string
    def insert_db_data(self, table, row_string, db_data):
        try:
            self.dbcur.execute('INSERT INTO {} VALUES {}'.format(table, row_string), db_data)
            self.dbcon.commit()
        except Exception as e:
            raise PysqliteException('Pysqlite experienced the following exception: {}'.format(e))

    # insert a list of rows into a db
    def insert_rows_to_db(self, table, row_string, db_data_list):
        if len(db_data_list) == 0:
            raise PysqliteException('Pysqlite received no data to input')
        if len(db_data_list) == 1:
            self.insert_db_data(table, row_string, db_data_list[0])
        else:
            for data_row in db_data_list:
                try:
                    self.dbcur.execute('INSERT INTO {} VALUES {}'.format(table, row_string), data_row)
                except Exception as e:
                    raise PysqliteException('Pysqlite could not insert a row: {}'.format(e))
                try:
                    self.dbcon.commit()
                except Exception as e:
                    raise PysqliteException('Pysqlite could not commit the data: {}'.format(e))

    def delete_row(self):
        # raise an exception if the row does not exist

        pass
