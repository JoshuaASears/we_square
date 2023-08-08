
-- create transactions table
CREATE TABLE IF NOT EXISTS  transactions(
    -- columns
    tId INTEGER,
    ledgerId INTEGER NOT NULL,
    item TEXT NOT NULL,
    amount TEXT NOT NULL,
    date TEXT NOT NULL,
    paidBy TEXT NOT NULL,
    itemEdited INTEGER DEFAULT 0,
    amountEdited INTEGER DEFAULT 0,
    dateEdited INTEGER DEFAULT 0,
    paidByEdited INTEGER DEFAULT 0,
    deleted INTEGER DEFAULT 0,
    -- constraints
    PRIMARY KEY (tId),
    CONSTRAINT ledgerCascade
        FOREIGN KEY (ledgerId)
        REFERENCES ledgers (lId)
        ON DELETE CASCADE);

-- create people table
CREATE TABLE IF NOT EXISTS people(
    -- columns
    pId INTEGER,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    ledgerId INTEGER NOT NULL,
    -- constraints
    PRIMARY KEY(pId),
    CONSTRAINT ledgerCascade
        FOREIGN KEY(ledgerId)
        REFERENCES ledgers (lId)
        ON DELETE CASCADE);

-- create ledgers table
CREATE TABLE IF NOT EXISTS ledgers(
    -- columns
    lId INTEGER,
    title TEXT NOT NULL,
    -- constraints
        PRIMARY KEY(lId));