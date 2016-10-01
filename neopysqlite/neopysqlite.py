import os
import sqlite3
import neopysqlite.exceptions as exception


class Pysqlite:
    # Initialise the class, make sure the file is accessible and open a connection
    def __init__(self, database_name, db_path, verbose=False):
        self.db_name = database_name
        self.db_path = db_path
        self.verbose = verbose
        self.dbcon = None
        self.dbcur = None
        self.connection_open = False
        self.table_names = []
        self.validate_database()

    def print(self, print_string):
        if self.verbose:
            print('[NPYSL] ' + print_string)

    def validate_database(self):
        self.print('Validating object for {}'.format(self.db_name))
        if os.path.isfile(self.db_path) and os.access(self.db_path, os.R_OK):
            self.dbcon = sqlite3.connect(self.db_path)
            self.dbcur = self.dbcon.cursor()
            self.print('Pysqlite successfully opened database connection to: {}'.format(self.db_name))
            self.connection_open = True
            self.update_table_names()
        else:
            raise exception.PysqliteCannotAccessException(db_name=self.db_name)

    def check_table_exists(self, table):
        self.update_table_names()
        if table not in self.table_names:
            raise exception.PysqliteTableDoesNotExist

    def update_table_names(self):
        self.table_names = self.get_table_names()

    def get_table_names(self):
        tables = self.get_specific_rows(table='sqlite_master', contents_string='name', filter_string='type = \'table\'')
        tables = [name[0] for name in tables]
        return tables

    def close_connection(self):
        self.print('Closing connection to database: {}'.format(self.db_name))
        self.dbcon.close()
        self.print('Connection closed to database: {}'.format(self.db_name))
        self.dbcon = None
        self.dbcur = None
        self.connection_open = False

    def execute_sql(self, sql_string, data=()):
        try:
            return self.dbcur.execute(sql_string, data)
        except sqlite3.OperationalError:
            raise exception.PysqliteExecutionException('SQLite3 threw an operational exception, check for mistakes in your SQL')
        except Exception:
            raise exception.PysqliteSQLExecutionException(db_name=self.db_name, sql_string=sql_string)

    def get_all_rows(self, table):
        try:
            db_data = self.execute_sql('SELECT * FROM {}'.format(table))
        except Exception:
            raise exception.PysqliteCouldNotRetrieveData(db_name=self.db_name, table_name=table)
        return [row for row in db_data]

    def get_specific_rows(self, table, contents_string='*', filter_string=''):
        try:
            db_data = self.execute_sql('SELECT {} FROM {} WHERE {}'.format(contents_string, table, filter_string))
        except Exception:
            raise exception.PysqliteCouldNotRetrieveData(db_name=self.db_name, table_name=table, filter_string=filter_string)
        data_list = [row for row in db_data]
        return data_list

    def insert_row(self, table, row_string, row_data):
        try:
            self.execute_sql('INSERT INTO {} VALUES {}'.format(table, row_string), row_data)
            self.dbcon.commit()
        except Exception:
            raise exception.PysqliteCouldNotInsertRow(db_name=self.db_name, table_name=table, data_row=row_data)

    def insert_rows(self, table, row_string, row_data_list):
        for row_data in row_data_list:
            try:
                self.execute_sql('INSERT INTO {} VALUES {}'.format(table, row_string), row_data)
                self.dbcon.commit()
            except Exception:
                raise exception.PysqliteCouldNotInsertRow(db_name=self.db_name, table_name=table, data_row=row_data)

    def delete_rows(self, table, delete_string='', delete_value=()):
        self.check_table_exists(table=table)
        execution_string = 'DELETE FROM {}'.format(table)
        if not delete_string == '':
            execution_string += ' WHERE {}'.format(delete_string)
        try:
            self.execute_sql(execution_string, delete_value)
            self.dbcon.commit()
        except Exception as e:
            raise exception.PysqliteCouldNotDeleteRow('Could not perform the deletion: {}'.format(e))

    def delete_all_rows(self, table):
        self.delete_rows(table=table)
