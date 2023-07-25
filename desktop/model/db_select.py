import desktop.data.schema as schema


def retrieve_ledger_titles(app):
    ledger_list = []
    for ledger in app.ledgers:
        ledger_list.append(ledger.get_title())
    return ledger_list


def retrieve_ledger_index_by_title(app, title):
    for index, ledger in enumerate(app.ledgers):
        if ledger.get_title() == title:
            return index
