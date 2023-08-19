
-- create ledgers table
CREATE TABLE IF NOT EXISTS ledgers(
    -- columns
    ledger_id INTEGER,
    title TEXT NOT NULL,
    -- constraints
    PRIMARY KEY(ledger_id));

-- create people table
CREATE TABLE IF NOT EXISTS people(
    -- columns
    people_id INTEGER,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    ledger_id INTEGER NOT NULL,
    -- constraints
    PRIMARY KEY(people_id),
    FOREIGN KEY(ledger_id)
        REFERENCES ledgers (ledger_id)
        ON DELETE CASCADE);

-- create transactions table
CREATE TABLE IF NOT EXISTS  transactions(
    -- columns
    transaction_id INTEGER,
    ledger_id INTEGER NOT NULL,
    item TEXT NOT NULL,
    amount TEXT NOT NULL,
    date TEXT NOT NULL,
    paid_by TEXT NOT NULL,
    item_edited INTEGER DEFAULT 0,
    amount_edited INTEGER DEFAULT 0,
    date_edited INTEGER DEFAULT 0,
    paid_by_edited INTEGER DEFAULT 0,
    deleted INTEGER DEFAULT 0,
    -- constraints
    PRIMARY KEY (transaction_id),
    FOREIGN KEY (ledger_id)
        REFERENCES ledgers (ledger_id)
        ON DELETE CASCADE);
