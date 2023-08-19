
import sqlite3

class DatabaseOperations:
    def __init__(self):
        self._connection = sqlite3.connect(".\\data\\data.db")
        self._cursor = self._connection.cursor()

        # foreign key check must be enabled on start up for SQLite
        self._connection.execute("PRAGMA foreign_keys = 1")
        # initialize tables
        self.create_tables()

    def close(self):
        self._connection.commit()
        self._connection.close()

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    #
    #           CREATE, SET, UPDATE, DELETE
    #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def create_tables(self):
        with open('.\\data\\schema.sql', 'r') as schema_file:
            sql_script = schema_file.read()
        self._cursor.executescript(sql_script)
        self._connection.commit()

    def delete_ledger(self, ledger_id: int):
        sql = """
                DELETE FROM ledgers
                where ledger_id = ?;
                """
        parameters = (ledger_id,)
        self._cursor.execute(sql, parameters)
        self._connection.commit()

    def record_ledger(self, title: str):
        sql = """
            INSERT INTO ledgers(title)
            VALUES(?);
        """
        parameters = (title,)
        self._cursor.execute(sql, parameters)
        self._connection.commit()

    def record_person(self, name: str, email: str, ledger_id: int):
        sql = """
            INSERT INTO people(name, email, ledger_id)
            VALUES (?, ?, ?);
        """
        parameters = (name, email, ledger_id)
        self._cursor.execute(sql, parameters)
        self._connection.commit()

    def record_transaction(self, ledger_id: int,
                           values: tuple[str, str, str, str]):
        sql = """
            INSERT INTO transactions(ledger_id, item, amount, date, paid_by)
            VALUES(?, ?, ?, ?, ?);
        """
        parameters = (ledger_id, values[0], values[1], values[2], values[3])
        self._cursor.execute(sql, parameters)
        self._connection.commit()

    def update_transaction(self, transaction_id: int,
                           old_values: tuple[str, str, str, str],
                           new_values: tuple[str, str, str, str]):
        columns = []
        values = []
        # compare and add to update if new
        if new_values[0] != old_values[0]:
            columns = columns + ["item", "item_edited", ]
            values = values + [new_values[0], 1]
        if new_values[1] != old_values[1]:
            columns = columns + ["amount", "amount_edited", ]
            values = values + [new_values[1], 1]
        if new_values[2] != old_values[2]:
            columns = columns + ["date", "date_edited", ]
            values = values + [new_values[2], 1]
        if new_values[3] != old_values[3]:
            columns = columns + ["paid_by", "paid_by_edited", ]
            values = values + [new_values[3], 1]
        if columns:
            sql = "UPDATE transactions SET "
            for index in range(len(columns)):
                sql += str(columns[index]) + " = '" + str(values[index]) + "'"
                if index != len(columns) - 1:
                    sql += ", "
            sql +=" WHERE transaction_id = ?;"
            parameters = (transaction_id,)
            self._cursor.execute(sql, parameters)
            self._connection.commit()

    def update_transaction_deleted(self, transaction_id: int):
        sql = """
            UPDATE transactions
            SET deleted = 1
            WHERE transaction_id = ?;
        """
        parameters = (transaction_id,)
        self._cursor.execute(sql, parameters)
        self._connection.commit()

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    #
    #           SELECT
    #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def retrieve_ledger_id_from_title(self, title: str) -> int | None:
        """Takes a str. Returns int or None."""
        sql = """
            SELECT ledger_id
            FROM ledgers
            WHERE title = ?;
            """
        parameters = (title,)
        results = self._cursor.execute(sql, parameters)
        # returns none or tuple
        ledger_id = results.fetchone()
        # return non or int value within tuple
        if ledger_id:
            return ledger_id[0]
        return None

    def retrieve_title_from_ledger_id(self, ledger_id: int) -> str:
        """Takes an int. Returns str."""
        sql = """
            SELECT title
            FROM ledgers
            WHERE ledger_id = ?;
            """
        parameters = (ledger_id,)
        results = self._cursor.execute(sql, parameters)
        title = results.fetchone()[0]
        return title

    def retrieve_ledgers_titles(self) -> list[str]:
        """Returns ["title1", "title2",...]"""
        sql = """
            SELECT title
            FROM ledgers;
            """
        results = self._cursor.execute(sql)
        ledgers_list = results.fetchall()

        ledgers_list = [x[0] for x in ledgers_list]
        return ledgers_list

    def retrieve_names_by_ledger_id(self, ledger_id: int) -> list[str]:
        """Takes int. Returns ["name1", "name2",...]"""
        sql = """
            SELECT name
            FROM people
            where ledger_id = ?;
            """
        parameters = (ledger_id,)
        results = self._cursor.execute(sql, parameters)
        people = results.fetchall()
        people = [x[0] for x in people]
        return people

    def retrieve_names_and_email_by_ledger_id(self, ledger_id: int) \
            -> list[tuple[str, str]]:
        """Takes int. Returns [("name1", "email1"), ("name2", "email2"),...]"""
        sql = """
            SELECT name, email
            FROM people
            where ledger_id = ?;
            """
        parameters = (ledger_id,)
        results = self._cursor.execute(sql, parameters)
        people = results.fetchall()
        return people

    def retrieve_transactions_by_ledger_id(self, ledger_id: int) \
            -> list[tuple[int, str, str, str, str, int, int, int, int, int]]:
        """
        Takes int. Returns [(transaction1), (transaction2),...]
        where transaction is a 10-tuple with the following indexing:
            [0]: transaction_id1,
            [1]: "item",        [2] "amount",           [3]: "date",
            [4] "paid_by",      [5]: item_edited,       [6]: amount_edited,
            [7]: date_edited,   [8]: paid_by_edited,    [9] deleted
        and indexes 5-9 are 0 or 1 integers as boolean values.
        """
        sql = """
            SELECT 
                transaction_id, 
                item, amount, date, paid_by,
                item_edited, amount_edited, date_edited, paid_by_edited,
                deleted
            FROM transactions
            WHERE ledger_id = ?;
            """
        parameters = (ledger_id,)
        results = self._cursor.execute(sql, parameters)
        transactions = results.fetchall()
        return transactions

    def retrieve_transaction_from_transaction_id(self, transaction_id: int) \
        -> tuple[str, str, str, str]:
        """Takes an int.
        Returns ("item", "amount", "date", "paid_by")"
        """
        sql = """
            SELECT item, amount, date, paid_by
            FROM transactions
            WHERE transaction_id = ?;
            """
        parameters = (transaction_id,)
        results = self._cursor.execute(sql, parameters)
        transaction = results.fetchone()
        return transaction
