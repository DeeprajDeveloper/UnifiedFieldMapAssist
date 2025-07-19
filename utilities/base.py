import sqlite3 as sql


class DBConnection:
    def __init__(self, database):
        self.database = database

    def connect(self):
        return sql.connect(self.database)

    def with_connection(self):
        """Context manager to use 'with' statement."""
        return self.connect()


class ErrorClass(Exception):
    def __init__(self, error_message, error_code):
        self.error_code = error_code
        self.error_message = error_message
        super().__init__(error_message)

