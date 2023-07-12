import sqlite3


def create_new_ledger(title_input, names):
    # connect to database and get cursor
    connection = sqlite3.connect("data.db")
    cursor = connection.cursor()

    ledger_title = ""
    for char in title_input:
        if char.isalpha():
            ledger_title += char
    people_title = ledger_title + "people"
    sql_ledger_table = \
        "CREATE TABLE {} (" \
        "t_id INTEGER NOT NULL," \
        "trans TEXT NOT NULL," \
        "amount TEXT NOT NULL," \
        "paid_by TEXT NOT NULL," \
        "date TEXT NOT NULL," \
        "PRIMARY KEY (t_id)," \
        "FOREIGN KEY (paid_by)" \
        "REFERENCES people (p_id)" \
        "ON DELETE NO ACTION" \
        ");".format(ledger_title)
    print(sql_ledger_table)
    sql_people_table = \
        "CREATE TABLE {} (" \
        "p_id INTEGER NOT NULL PRIMARY KEY," \
        "name TEXT NOT NULL," \
        "email TEXT NOT NULL" \
        ");".format(people_title)

    cursor.execute(sql_ledger_table)
    cursor.execute(sql_people_table)

    #TODO: INSERT INTO people_title ()

    connection.commit()
    connection.close()
