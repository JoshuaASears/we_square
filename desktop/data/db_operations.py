"""

NOTE ON OPERATIONS

    OPERATIONS REQUIRING A 'db_connection' PARAMETER:
        'db_connection' ARGUMENT PROVIDES METHODS WITH
            1. executescript_and_commit
            2. execute_and_commit
        USED FOR OPERATIONS THAT MAKE CHANGES TO THE DATABASE INCLUDING:
            CREATE, SET, UPDATE, DELETE

    OPERATIONS REQUIRING A 'cursor' PARAMETER:
        'cursor' ARGUMENT IS A REGULAR SQLite CURSOR OBJECT.
        USED BELOW FOR METHODS THAT ONLY EXECUTE SELECT QUERIES WITHOUT MAKING
        CHANGES TO THE DATABASE.

"""

# DATABASE OPERATIONS
def create_tables(db_connection):

    with open('.\\data\\schema.sql', 'r') as schema_file:
        sql_script = schema_file.read()

    db_connection.executescript_and_commit(sql_script)


# LEDGERS OPERATIONS
def create_ledger(db_connection, title: str, people: list):
    """Returns an integer."""
    # log ledger in ledger table
    sql = """
        INSERT INTO ledgers(title)
        VALUES(?);
    """
    parameters = (title,)
    db_connection.execute_and_commit(sql, parameters)
    # get ledger ledger id for new ledger entry
    ledger_id = retrieve_lId_from_title(
        cursor=db_connection.get_cursor(),
        title=title)
    # log people
    for person in people:
        sql = """
            INSERT INTO people(name, email, ledgerId)
            VALUES(?, ?, ?);
        """
        parameters = (person["name"], person["email"], ledger_id)
        db_connection.execute_and_commit(sql, parameters)
    return ledger_id

def retrieve_lId_from_title(cursor, title):
    """Returns an integer or None."""
    sql = """
        SELECT lId
        FROM ledgers
        WHERE title = ?;
        """
    parameters = (title,)
    results = cursor.execute(sql, parameters)
    # returns none or tuple
    ledger_id = results.fetchone()
    # return non or int value within tuple
    if ledger_id:
        return ledger_id[0]
    return None

def retrieve_title_from_lId(cursor, ledger_id):
    """Returns a string."""
    sql = """
        SELECT title
        FROM ledgers
        WHERE lId = ?;
        """
    parameters = (ledger_id,)
    results = cursor.execute(sql, parameters)
    title = results.fetchone()[0]
    return title

def retrieve_ledgers_list(cursor):
    """
    Returns a list of strings ['ledger1', 'legder2',...] or empty list.
    """
    sql = """
        SELECT title
        FROM ledgers;
        """
    results = cursor.execute(sql)
    ledgers_list = results.fetchall()

    ledgers_list = [x[0] for x in ledgers_list]
    return ledgers_list

def delete_ledger(db_connection, ledger_id):
    sql = """
        DELETE FROM ledgers
        where lId = ?;
        """
    parameters = (ledger_id,)
    db_connection.execute_and_commit(sql, parameters)

# PEOPLE OPERATIONS
def retrieve_people_on_ledger(cursor, ledger_id):
    """
    Returns a list of strings ['person1', 'person2',...] or empty list.
    """
    sql = """
        SELECT name
        FROM people
        where ledgerId = ?;
        """
    parameters = (ledger_id,)
    results = cursor.execute(sql, parameters)
    people = results.fetchall()
    people = [x[0] for x in people]
    return people

# TRANSACTIONS OPERATIONS
def create_transaction(db_connection, ledger_id, values):
    sql = """
        INSERT INTO transactions(ledgerId, item, amount, date, paidBy)
        VALUES(?, ?, ?, ?, ?);
    """
    parameters = (ledger_id, values[0], values[1], values[2], values[3])
    db_connection.execute_and_commit(sql, parameters)

def retrieve_transactions(cursor, ledger_id):
    """
    Returns a list of 10-tuples:
    [(tId, item, amount, date, paid by,
    itemEdited, amountEdited, dateEdited, paidByEdited, deleted),]
    or empty list.
    """
    sql = """
        SELECT *
        FROM transactions
        WHERE ledgerId = ?;
        """
    parameters = (ledger_id,)
    results = cursor.execute(sql, parameters)
    transactions = results.fetchall()
    return transactions

def retrieve_transaction_from_tId(cursor, transaction_id):
    sql = """
        SELECT tId, item, amount, date, paidBy
        FROM transactions
        WHERE tId = ?;
        """
    parameters = (transaction_id,)
    results = cursor.execute(sql, parameters)
    transaction = results.fetchone()
    return transaction

def update_transaction(db_connection, transaction_id, old_values, new_values):
    columns = []
    values = []
    # compare and add to update if new
    if new_values[0] != old_values[0]:
        columns = columns + ["item", "itemEdited", ]
        values = values + [new_values[0], 1]
    if new_values[1] != old_values[1]:
        columns = columns + ["amount", "amountEdited", ]
        values = values + [new_values[1], 1]
    if new_values[2] != old_values[1]:
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
    db_connection.execute_and_commit(sql, parameters)


def mark_transaction_deleted(db_connection, transaction_id):
    sql = """
        UPDATE transactions
        SET deleted = 1
        WHERE tId = ?;
    """
    parameters = (transaction_id,)
    db_connection.execute_and_commit(sql, parameters)

# SUMMARY OPERATIONS
def get_ledger_summary():
    pass

