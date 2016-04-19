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


class PysqliteTableDoesNotExist(PysqliteException):
    def __init__(self, db_name, table_name):
        self.db_name = db_name
        self.table_name = table_name

    def __str__(self):
        return 'DB: {} does not have a table called: {}'


class PysqliteCouldNotDeleteRow(PysqliteException):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return self.value


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
            # set the table names
            self.table_names = []
            self.update_table_names()
        else:
            raise PysqliteCannotAccessException(db_name=self.db_name)

    def get_table_names(self):
        tables = self.get_specific_db_data(table='sqlite_master', contents_string='name', filter_string='type = \'table\'')
        tables = [name[0] for name in tables]
        return tables

    def update_table_names(self):
        self.table_names = self.get_table_names()

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
    def get_specific_db_data(self, table, contents_string='*', filter_string=''):
        try:
            db_data = self.dbcur.execute('SELECT {} FROM {} WHERE {}'.format(contents_string, table, filter_string))
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

    # delete data according to a filter string
    def delete_data(self, table, delete_string='', delete_value=()):
        # check if the table is in the known table names
        if table not in self.table_names:
            # TODO: Check if python has lazy evaluation and rewrite this nested if
            if table not in self.get_table_names():
                raise PysqliteTableDoesNotExist(db_name=self.db_name, table_name=table)
        # if the table exists, delete the row
        try:
            if delete_string == '':
                self.dbcur.execute('DELETE FROM {}'.format(table))
            else:
                self.dbcur.execute('DELETE FROM {} WHERE {}'.format(table, delete_string), delete_value)
        except Exception as e:
            raise PysqliteCouldNotDeleteRow(e)
        # commit the deletion
        try:
            self.dbcon.commit()
        except Exception as e:
            raise PysqliteCouldNotDeleteRow('Could not commit the deletion: {}'.format(e))

    # delete all the data from a table
    def delete_all_data(self, table):
        self.delete_data(table=table, delete_string='')
