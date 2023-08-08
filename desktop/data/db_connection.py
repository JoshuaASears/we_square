import sqlite3

import desktop.data.db_operations as app_model

class DBConnection:

    def __init__(self):
        self._connection = sqlite3.connect(".\\data\\data.db")
        self._cursor = self._connection.cursor()

        # foreign key check must be enabled on start up for SQLite
        self._connection.execute("PRAGMA foreign_keys = 1")
        # initialize tables
        app_model.create_tables(self)

    def commit(self):
        self._connection.commit()

    def close_connection(self):
        self._connection.close()

    def commit_and_close(self):
        self.commit()
        self.close_connection()

    def execute_and_commit(self, sql, parameters):
        results = self._cursor.execute(sql, parameters)
        self.commit()
        return results

    def executescript_and_commit(self, sql_script):
        self._cursor.executescript(sql_script)
        self.commit()

    def get_cursor(self):
        return self._cursor
