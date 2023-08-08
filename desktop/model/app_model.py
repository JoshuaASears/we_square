
from desktop.data.db_operations import DatabaseOperations

import datetime
import json

class AppModel:

    def __init__(self):
        self._db_connection = DatabaseOperations()
        self._current_ledger = None
        self._transaction_being_updated = None

    def close_connection(self):
        self._db_connection.close()
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    #
    #           GETTERS AND SETTERS
    #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def get_current_ledger(self):
        return self._current_ledger

    def set_current_ledger(self, ledger_id):
        self._current_ledger = ledger_id

    def set_ledger_from_title(self, title):
        ledger_id = self._db_connection.retrieve_lId_from_title(title)
        self.set_current_ledger(ledger_id)

    def set_transaction_being_updated(self, transaction):
        self._transaction_being_updated = transaction

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    #
    #           CREATE
    #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def create_and_set_ledger(self, title, people):
        self._db_connection.record_ledger(title)
        ledger_id = self._db_connection.retrieve_lId_from_title(title)
        for person in people:
            self._db_connection.record_person(
                name=person[0],
                email=person[1],
                ledger_id=ledger_id,
            )
        self.set_current_ledger(ledger_id)

    def create_or_update_transaction(self, values):
        if self._transaction_being_updated:
            self.update_transaction(values)
            self._transaction_being_updated = None
            return True
        else:
            self._db_connection.record_transaction(
                ledger_id=self._current_ledger,
                values=values
            )

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    #
    #           RETRIEVE
    #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def retrieve_and_store_transaction_values(self, transaction_id):
        transaction = self._db_connection.retrieve_transaction_from_tId(
            transaction_id=transaction_id
        )
        self._transaction_being_updated = transaction
        return transaction[1:]

    def retrieve_ledgers_list(self):
        ledger_list = self._db_connection.retrieve_ledgers_titles(
        )
        return ledger_list

    def retrieve_lId_from_title(self, title):
        ledger_id = self._db_connection.retrieve_lId_from_title(
            title=title,
        )
        return ledger_id

    def retrieve_people_name_and_email(self):
        people_name_and_email = self._db_connection.retrieve_people_and_email_by_lId(
            ledger_id=self._current_ledger
        )
        return people_name_and_email

    def retrieve_people_on_ledger(self):
        people = self._db_connection.retrieve_people_by_lId(
            ledger_id=self._current_ledger
        )
        return people

    def retrieve_title_from_lId(self):
        title = self._db_connection.retrieve_title_from_lId(
            ledger_id=self._current_ledger
        )
        return title

    def retrieve_transactions(self):
        transactions = self._db_connection.retrieve_transactions_by_lId(
            ledger_id=self._current_ledger
        )
        return transactions

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    #
    #           UPDATE
    #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def update_transaction(self, values):
        self._db_connection.update_transaction(
            transaction_id=self._transaction_being_updated[0],
            old_values=self._transaction_being_updated[1:],
            new_values=values,
        )

    def mark_transaction_deleted(self, transaction_id):
        self._db_connection.update_transaction_deleted(
            transaction_id=transaction_id
        )
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    #
    #           DELETE
    #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def delete_ledger(self):
        self._db_connection.delete_ledger(
            ledger_id=self._current_ledger
        )
        self._current_ledger = None

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    #
    #           COMPOSITE LOGIC
    #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    @staticmethod
    def make_summary():
        #TODO: calculations from ledger for string
        summary = ""
        return summary

    def get_modified_transactions(self):
        transactions = self.retrieve_transactions()
        # present transaction values with edited/deleted markup
        modified_transactions = []
        for transaction in transactions:
            item = transaction[1]
            amount = transaction[2]
            date = transaction[3]
            paidBy = transaction[4]
            if transaction[5]:
                item += "*"
            if transaction[6]:
                amount += "*"
            if transaction[7]:
                date += "*"
            if transaction[8]:
                paidBy += "*"
            if transaction[9]:
                item = "(X)" + item
            modified_transactions.append((
                transaction[0], item, amount, date, paidBy))
        return modified_transactions

    def convert_people_data_for_json(self):
        people_data = self.retrieve_people_name_and_email()
        people = {"people": []}
        for person_data in people_data:
            people["people"].append({
                "name": person_data[0],
                "email": person_data[1]})
        return people

    def convert_transactions_for_json(self):
        transaction_data = self.get_modified_transactions()
        transactions = {"items": []}
        for transaction in transaction_data:
            transactions["items"].append(
                {
                "item": transaction[1],
                "amount": transaction[2],
                "date": transaction[3],
                "paid_by": transaction[4],
            })
        return transactions

    def send_ledger(self):
        title = {"title": self.retrieve_title_from_lId()}
        summary = {"summary": "[PLACEHOLDER FOR NOW]"}
        people = self.convert_people_data_for_json()
        transactions = self.convert_transactions_for_json()
        date = {"date": str(datetime.date.today())}

        ledger_data = {"ledger": [title, summary, people, transactions, date]}

        #TODO: Incorporate microservice templater and send email

        data = json.dumps(obj=ledger_data, indent=4)

        with open("new_sample.json", "w") as outfile:
            outfile.write(data)

