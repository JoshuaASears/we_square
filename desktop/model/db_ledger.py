import desktop.data.schema as schema


def retrieve_title(ledger: schema.Ledger):
    return ledger.get_title()


def retrieve_persons(ledger: schema.Ledger):
    person_list = []
    for person in ledger.get_persons():
        person_list.append(person.get_name())
    return person_list


def retrieve_transactions(ledger: schema.Ledger):
    transactions = ledger.get_transactions()
    item_list = []
    for transaction in transactions:
        if not transaction.is_deleted():
            item = transaction.get_item()
            amount = transaction.get_amount()
            date = transaction.get_date()
            paid_by = transaction.get_paid_by()
            item_list.append((item, amount, date, paid_by))
    return item_list


def add_transaction(
        ledger: schema.Ledger,
        item,
        amount,
        date,
        paid_by,
        key,
):
    if key:
        transaction = ledger.get_transaction_from_id(key)
        if transaction.get_item() != item:
            transaction.set_item(item)
        if transaction.get_amount() != amount:
            transaction.set_amount(amount)
        if transaction.get_date() != date:
            transaction.set_date(date)
        if transaction.get_paid_by() != paid_by:
            transaction.set_paid_by(paid_by)

    else:
        transaction = schema.Transaction(item, amount, date, paid_by)
        ledger.add_transaction(transaction)


def delete_transaction(
        ledger: schema.Ledger,
        key: int
):
    transaction = ledger.get_transaction_from_id(key)
    transaction.delete()
