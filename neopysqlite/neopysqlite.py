import os
import sqlite3
import neopysqlite.exceptions as exception


class Pysqlite:
    # Initialise the class, make sure the file is accessible and open a connection
    def __init__(self, database_name='', database_file='', verbose=False):
        self.db_name = database_name
        self.verbose = verbose
        self.print('Pysqlite object for {} initialising'.format(self.db_name))
        # Check if the database exists and if we can properly access it
        if os.path.isfile(database_file) and os.access(database_file, os.R_OK):
            self.dbcon = sqlite3.connect(database_file)
            self.dbcur = self.dbcon.cursor()
            self.print('Pysqlite successfully opened database connection to: {}'.format(self.db_name))
            # set the table names
            self.table_names = []
            self.update_table_names()
        else:
            raise exception.PysqliteCannotAccessException(db_name=self.db_name)

    def print(self, print_string):
        if self.verbose:
            print('[NPYSL] ' + print_string)

    def get_table_names(self):
        tables = self.get_specific_rows(table='sqlite_master', contents_string='name', filter_string='type = \'table\'')
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
        except Exception:
            raise exception.PysqliteSQLExecutionException(db_name=self.db_name, execution_string=execution_string)

    # get all the data in a table as a list
    def get_all_rows(self, table):
        try:
            db_data = self.dbcur.execute('SELECT * FROM {}'.format(table))
        except Exception:
            raise exception.PysqliteCouldNotRetrieveData(db_name=self.db_name, table_name=table)
        data_list = [row for row in db_data]
        return data_list

    # get data from a table whilst passing an SQL filter condition
    def get_specific_rows(self, table, contents_string='*', filter_string=''):
        try:
            db_data = self.dbcur.execute('SELECT {} FROM {} WHERE {}'.format(contents_string, table, filter_string))
        except Exception:
            raise exception.PysqliteCouldNotRetrieveData(db_name=self.db_name, table_name=table, filter_string=filter_string)
        data_list = [row for row in db_data]
        return data_list

    # insert a row to a table, pass the schema of the row as the row_string
    def insert_row(self, table, row_string, row_data):
        try:
            self.dbcur.execute('INSERT INTO {} VALUES {}'.format(table, row_string), row_data)
            self.dbcon.commit()
        except Exception:
            raise exception.PysqliteCouldNotInsertRow(db_name=self.db_name, table_name=table, data_row=row_data)

    # insert a list of rows into a db
    def insert_rows(self, table, row_string, row_data_list):
        if len(row_data_list) == 0:
            raise exception.PysqliteException('Pysqlite received no data to input')
        if len(row_data_list) == 1:
            self.insert_row(table, row_string, row_data_list[0])
        else:
            for row_data in row_data_list:
                try:
                    self.dbcur.execute('INSERT INTO {} VALUES {}'.format(table, row_string), row_data)
                except Exception as e:
                    raise exception.PysqliteCouldNotInsertRow(db_name=self.db_name, table_name=table, data_row=row_data)
                try:
                    self.dbcon.commit()
                except Exception as e:
                    raise exception.PysqliteException('Pysqlite could not commit the data: {}'.format(e))

    # delete data according to a filter string
    def delete_rows(self, table, delete_string='', delete_value=()):
        # check if the table is in the known table names
        if table not in self.table_names:
            # TODO: Check if python has lazy evaluation and rewrite this nested if statement
            if table not in self.get_table_names():
                raise exception.PysqliteTableDoesNotExist(db_name=self.db_name, table_name=table)
        # if the table exists, delete the row
        try:
            if delete_string == '':
                self.dbcur.execute('DELETE FROM {}'.format(table))
            else:
                self.dbcur.execute('DELETE FROM {} WHERE {}'.format(table, delete_string), delete_value)
        except Exception as e:
            raise exception.PysqliteCouldNotDeleteRow('Could not perform the deletion: {}'.format(e))
        # commit the deletion
        try:
            self.dbcon.commit()
        except Exception as e:
            raise exception.PysqliteCouldNotDeleteRow('Could not commit the deletion: {}'.format(e))

    # delete all the data from a table
    def delete_all_rows(self, table):
        self.delete_rows(table=table, delete_string='')
