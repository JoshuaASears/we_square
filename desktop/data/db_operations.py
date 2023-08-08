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

    def record_ledger(self, title):
        sql = """
            INSERT INTO ledgers(title)
            VALUES(?);
        """
        parameters = (title,)
        self._cursor.execute(sql, parameters)
        self._connection.commit()

    def record_person(self, name, email, ledger_id):
        sql = """
            INSERT INTO people(name, email, ledgerId)
            VALUES (?, ?, ?);
        """
        parameters = (name, email, ledger_id)
        self._cursor.execute(sql, parameters)
        self._connection.commit()

    def delete_ledger(self, ledger_id):
        sql = """
                DELETE FROM ledgers
                where lId = ?;
                """
        parameters = (ledger_id,)
        self._cursor.execute(sql, parameters)
        self._connection.commit()

    def record_transaction(self, ledger_id, values):
        sql = """
            INSERT INTO transactions(ledgerId, item, amount, date, paidBy)
            VALUES(?, ?, ?, ?, ?);
        """
        parameters = (ledger_id, values[0], values[1], values[2], values[3])
        self._cursor.execute(sql, parameters)
        self._connection.commit()

    def update_transaction(self, transaction_id, old_values, new_values):
        columns = []
        values = []
        # compare and add to update if new
        if new_values[0] != old_values[0]:
            columns = columns + ["item", "itemEdited", ]
            values = values + [new_values[0], 1]
        if new_values[1] != old_values[1]:
            columns = columns + ["amount", "amountEdited", ]
            values = values + [new_values[1], 1]
        if new_values[2] != old_values[2]:
            columns = columns + ["date", "dateEdited", ]
            values = values + [new_values[2], 1]
        if new_values[3] != old_values[3]:
            columns = columns + ["paidBy", "paidByEdited", ]
            values = values + [new_values[3], 1]

        sql = "UPDATE transactions SET "
        for index in range(len(columns)):
            sql += str(columns[index]) + " = '" + str(values[index]) + "'"
            if index != len(columns) - 1:
                sql += ", "
        sql +=" WHERE tId = ?;"
        parameters = (transaction_id,)
        self._cursor.execute(sql, parameters)
        self._connection.commit()

    def update_transaction_deleted(self, transaction_id):
        sql = """
            UPDATE transactions
            SET deleted = 1
            WHERE tId = ?;
        """
        parameters = (transaction_id,)
        self._cursor.execute(sql, parameters)
        self._connection.commit()

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    #
    #           SELECT
    #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def retrieve_lId_from_title(self, title):
        sql = """
            SELECT lId
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

    def retrieve_title_from_lId(self, ledger_id):
        sql = """
            SELECT title
            FROM ledgers
            WHERE lId = ?;
            """
        parameters = (ledger_id,)
        results = self._cursor.execute(sql, parameters)
        title = results.fetchone()[0]
        return title

    def retrieve_ledgers_titles(self):
        sql = """
            SELECT title
            FROM ledgers;
            """
        results = self._cursor.execute(sql)
        ledgers_list = results.fetchall()

        ledgers_list = [x[0] for x in ledgers_list]
        return ledgers_list

    def retrieve_people_by_lId(self, ledger_id):
        sql = """
            SELECT name
            FROM people
            where ledgerId = ?;
            """
        parameters = (ledger_id,)
        results = self._cursor.execute(sql, parameters)
        people = results.fetchall()
        people = [x[0] for x in people]
        return people

    def retrieve_people_and_email_by_lId(self, ledger_id):
        sql = """
                    SELECT name, email
                    FROM people
                    where ledgerId = ?;
                    """
        parameters = (ledger_id,)
        results = self._cursor.execute(sql, parameters)
        people = results.fetchall()
        return people

    def retrieve_transactions_by_lId(self, ledger_id):
        sql = """
            SELECT 
                tId, 
                item, amount, date, paidBy,
                itemEdited, amountEdited, dateEdited, paidByEdited,
                deleted
            FROM transactions
            WHERE ledgerId = ?;
            """
        parameters = (ledger_id,)
        results = self._cursor.execute(sql, parameters)
        transactions = results.fetchall()
        return transactions

    def retrieve_transaction_from_tId(self, transaction_id):
        sql = """
            SELECT tId, item, amount, date, paidBy
            FROM transactions
            WHERE tId = ?;
            """
        parameters = (transaction_id,)
        results = self._cursor.execute(sql, parameters)
        transaction = results.fetchone()
        return transaction

    def get_ledger_summary(self):
        pass

