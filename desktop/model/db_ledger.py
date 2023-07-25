import desktop.data.schema as schema


def retrieve_title(ledger: schema.Ledger):
    return ledger.get_title()


def retrieve_title_for_json(ledger: schema.Ledger):
    return {"title": ledger.get_title()}


def retrieve_summary(ledger: schema.Ledger):
    return ledger.get_summary()


def retrieve_summary_for_json(ledger: schema.Ledger):
    return {"summary": ledger.get_summary()}


def retrieve_persons_for_json(ledger: schema.Ledger):
    person_data = []
    for person in ledger.get_persons():
        person_data.append({
            "name": person.get_name(),
            "email": person.get_email()
        })
    return {"persons": person_data}


def retrieve_person_names(ledger: schema.Ledger):
    person_list = []
    for person in ledger.get_persons():
        person_list.append(person.get_name())
    return person_list


def retrieve_transactions(ledger: schema.Ledger):

    transactions = ledger.get_transactions()
    item_list = []

    for transaction in transactions:
        data = transaction.get_transaction_data()
        item = data["item"][0]
        if data["item"][1]:
            item += "*"
        if data["deleted"] is True:
            item = "(del)" + item
        amount = data["amount"][0]
        if data["amount"][1]:
            amount += "*"
        date = data["date"][0]
        if data["date"][1]:
            date += "*"
        paid_by = data["paid_by"][0]
        if data["paid_by"][1]:
            paid_by += "*"

        item_list.append((item, amount, date, paid_by))

    return item_list


def retrieve_transactions_for_json(ledger: schema.Ledger):

    transactions = ledger.get_transactions()
    transaction_data = []
    
    for index, transaction in enumerate(transactions):
        data = transaction.get_transaction_data()
        if data["item"][1]:
            data["item"][0] += "*"
        data["item"] = data["item"][0]
        if data["deleted"] is True:
            data["item"] = "(del)" + data["item"][0]
        del data["deleted"]
        if data["amount"][1]:
            data["amount"][0] += "*"
        data["amount"] = data["amount"][0]
        if data["date"][1]:
            data["date"][0] += "*"
        data["date"] = data["date"][0]
        if data["paid_by"][1]:
            data["paid_by"][0] += "*"
        data["paid_by"] = data["paid_by"][0]
        transaction_data.append(data)

    return {"items": transaction_data}


def add_transaction(
        ledger: schema.Ledger,
        item,
        amount,
        date,
        paid_by,
        key=None,
):
    if key is not None:
        transaction = ledger.get_transaction_from_id(key)
        data = transaction.get_transaction_data()

        # update if not previously deleted
        if not data["deleted"]:
            # update values
            if data["item"][0] != item:
                transaction.set_item(item)
            if data["amount"][0] != amount:
                transaction.set_amount(amount)
            if data["date"][0] != date:
                transaction.set_date(date)
            if data["paid_by"][0] != paid_by:
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
