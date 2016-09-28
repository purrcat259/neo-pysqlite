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
            self.update_table_names()
        else:
            raise exception.PysqliteCannotAccessException(db_name=self.db_name)

    def get_table_names(self):
        tables = self.get_specific_rows(table='sqlite_master', contents_string='name', filter_string='type = \'table\'')
        tables = [name[0] for name in tables]
        return tables

    def update_table_names(self):
        self.table_names = self.get_table_names()

    def close_connection(self):
        self.dbcon.close()

    def execute_sql(self, sql_string):
        try:
            self.dbcur.execute(sql_string)
        except Exception:
            raise exception.PysqliteSQLExecutionException(db_name=self.db_name, sql_string=sql_string)

    def get_all_rows(self, table):
        try:
            db_data = self.dbcur.execute('SELECT * FROM {}'.format(table))
        except Exception:
            raise exception.PysqliteCouldNotRetrieveData(db_name=self.db_name, table_name=table)
        data_list = [row for row in db_data]
        return data_list

    def get_specific_rows(self, table, contents_string='*', filter_string=''):
        try:
            db_data = self.dbcur.execute('SELECT {} FROM {} WHERE {}'.format(contents_string, table, filter_string))
        except Exception:
            raise exception.PysqliteCouldNotRetrieveData(db_name=self.db_name, table_name=table, filter_string=filter_string)
        data_list = [row for row in db_data]
        return data_list

    def insert_row(self, table, row_string, row_data):
        try:
            self.dbcur.execute('INSERT INTO {} VALUES {}'.format(table, row_string), row_data)
            self.dbcon.commit()
        except Exception:
            raise exception.PysqliteCouldNotInsertRow(db_name=self.db_name, table_name=table, data_row=row_data)

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

    def delete_all_rows(self, table):
        self.delete_rows(table=table, delete_string='')
