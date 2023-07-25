import datetime


class Person:

    def __init__(
            self,
            name: str,
            email: str
    ):
        self._name = name
        self._email = email

    def get_name(self):
        return self._name

    def get_email(self):
        return self._email


class Transaction:

    def __init__(
            self,
            item: str,
            amount: str,
            date: datetime.date,
            paid_by: Person
    ):

        self._item = item
        self._item_modified = False

        self._amount = amount
        self._amount_modified = False

        self._date = date
        self._date_modified = False

        self._paid_by = paid_by
        self._paid_be_modified = False

        self._transaction_deleted = False

    def get_item(self):
        return self._item

    def get_amount(self):
        return self._amount

    def get_date(self):
        return self._date

    def get_paid_by(self):
        return self._paid_by

    def set_item(self, new_value):
        self._item = new_value
        self._item_modified = True

    def set_amount(self, new_value):
        self._amount = new_value
        self._amount_modified = True

    def set_date(self, new_value):
        self._date = new_value
        self._date_modified = True

    def set_paid_by(self, new_value):
        self._paid_by = new_value
        self._paid_be_modified = True

    def delete(self):
        self._transaction_deleted = True

    def is_deleted(self):
        return self._transaction_deleted


class Ledger:
    """Ledger objects have multiple Person Objects and Transaction Objects."""
    def __init__(self, title: str, persons: list):
        self._title = title
        self._persons = persons
        self._transaction_count = 0
        self._transactions = dict()
        self._summary = ""

    def get_title(self):
        return self._title

    def get_persons(self):
        return self._persons

    def get_transaction_from_id(self, index):
        return self._transactions[index]

    def get_transactions(self):
        transactions = []
        for count in range(self._transaction_count):
            transactions.append(self._transactions[count])
        return transactions

    def add_transaction(self, transaction):
        self._transactions[self._transaction_count] = transaction
        self._transaction_count += 1
