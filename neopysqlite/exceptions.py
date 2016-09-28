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


class PysqliteSQLExecutionException(PysqliteException):
    def __init__(self, db_name, execution_string):
        self.db_name = db_name
        self.execution_string = execution_string

    def __str__(self):
        return 'Could not execute the command: {} in the DB: {}'.format(self.execution_string, self.db_name)


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


class PysqliteCouldNotRetrieveData(PysqliteException):
    def __init__(self, db_name, table_name, filter_string=''):
        self.db_name = db_name
        self.table_name = table_name
        self.filter = filter_string

    def __str__(self):
        if self.filter == '':
            return 'Could not retrieve the data from table: {} in the DB: {}'.format(self.table_name, self.db_name)
        else:
            return 'Could not retrieve the data with filter: {} from table: {} in the DB: {}'.format(self.filter, self.table_name, self.db_name)


class PysqliteCouldNotInsertRow(PysqliteException):
    def __init__(self, db_name, table_name, data_row):
        self.db_name = db_name
        self.table_name = table_name
        self.data_row = data_row

    def __str__(self):
        return 'Could not insert data: {} in the table: {} in DB: {}'.format(self.data_row, self.table_name, self.db_name)