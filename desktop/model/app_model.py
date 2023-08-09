
from desktop.data.db_operations import DatabaseOperations

import datetime
import json
import math
import socket

class AppModel:

    def __init__(self):
        self._db_connection = DatabaseOperations()
        # ledger_id: int
        self._current_ledger = None
        # tuple(ledger_id("item", "amount", "date", "paid_by"))
        self._transaction_being_updated = None

    def close_connection(self):
        self._db_connection.close()

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    #
    #           GETTERS AND SETTERS
    #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def get_current_ledger(self) -> int:
        return self._current_ledger

    def set_current_ledger(self, ledger_id: int):
        self._current_ledger = ledger_id

    def set_ledger_from_title(self, title: str):
        ledger_id = self._db_connection.retrieve_ledger_id_from_title(title)
        self.set_current_ledger(ledger_id)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    #
    #           CREATE
    #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def create_and_set_ledger(self, title: str, people: list[tuple[str, str]]):
        self._db_connection.record_ledger(title)
        ledger_id = self._db_connection.retrieve_ledger_id_from_title(title)
        for person in people:
            self._db_connection.record_person(
                name=person[0],
                email=person[1],
                ledger_id=ledger_id,
            )
        self.set_current_ledger(ledger_id)

    def create_or_update_transaction(self, values: tuple[str, str, str, str]) \
            -> bool:
        if self._transaction_being_updated:
            self.update_transaction(values)
            self._transaction_being_updated = None
            return True
        else:
            self._db_connection.record_transaction(
                ledger_id=self._current_ledger,
                values=values
            )
            return False

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    #
    #           RETRIEVE
    #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def retrieve_and_store_transaction_values(self, transaction_id: int) \
            -> tuple[str, str, str, str]:
        transaction = \
            self._db_connection.retrieve_transaction_from_transaction_id(
            transaction_id=transaction_id
        )
        self._transaction_being_updated = transaction_id, transaction
        return transaction

    def retrieve_ledgers_list(self) -> list[str]:
        ledger_list = self._db_connection.retrieve_ledgers_titles(
        )
        return ledger_list

    def retrieve_ledger_id_from_title(self, title: str) -> int:
        ledger_id = self._db_connection.retrieve_ledger_id_from_title(
            title=title,
        )
        return ledger_id

    def retrieve_people_name_and_email(self) -> list[tuple[str, str]]:
        people_name_and_email = \
            self._db_connection.retrieve_names_and_email_by_ledger_id(
            ledger_id=self._current_ledger
        )
        return people_name_and_email

    def retrieve_names_on_ledger(self) -> list[str]:
        people = self._db_connection.retrieve_names_by_ledger_id(
            ledger_id=self._current_ledger
        )
        return people

    def retrieve_title_from_ledger_id(self) -> str:
        title = self._db_connection.retrieve_title_from_ledger_id(
            ledger_id=self._current_ledger
        )
        return title

    def retrieve_transactions(self) -> list[dict]:
        transactions = self._db_connection.retrieve_transactions_by_ledger_id(
            ledger_id=self._current_ledger
        )
        readable_transactions = []
        for transaction in transactions:
            transaction_dictionary = {
                "transaction_id":   transaction[0],
                "item":             transaction[1],
                "amount":           transaction[2],
                "date":             transaction[3],
                "paid_by":          transaction[4],
                "item_edited":      transaction[5],
                "amount_edited":    transaction[6],
                "date_edited":      transaction[7],
                "paid_by_edited":   transaction[8],
                "deleted":          transaction[9]
            }
            readable_transactions.append(transaction_dictionary)
        return readable_transactions

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    #
    #           UPDATE
    #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def update_transaction(self, values: tuple[str, str, str, str]):
        self._db_connection.update_transaction(
            transaction_id=self._transaction_being_updated[0],
            old_values=self._transaction_being_updated[1],
            new_values=values,
        )

    def mark_transaction_deleted(self, transaction_id: int):
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
    def make_summary(self):
        expense_total = 0.00
        people = self.retrieve_names_on_ledger()
        number_of_people = len(people)
        contributions = [0] * number_of_people
        # ex: people[0] has paid contributions[0] towards the expense_total

        transactions = self.retrieve_transactions()
        for transaction in transactions:
            # ignore deleted transactions
            if not transaction["deleted"]:
                # handling for transaction between parties on ledger
                if transaction["item"] in people:
                    # add to individual total (paid by)
                    index = people.index(transaction["paid_by"])
                    contributions[index] += float(transaction["amount"])
                    # subtract from individual total (person as item)
                    index = people.index(transaction["item"])
                    contributions[index] -= float(transaction["amount"])
                # regular transaction (purchase)
                else:
                    expense_total += float(transaction["amount"])
                    index = people.index(transaction["paid_by"])
                    contributions[index] += float(transaction["amount"])

        expense_total = round(expense_total, 2)
        expense_per_person = round((expense_total / number_of_people), 2)
        summary = f"Expense total: ${expense_total}\t" + \
                f"Total per person: ${expense_per_person}\n"
        we_square = True
        for index in range(len(people)):
            expense_difference = \
                round(expense_per_person - contributions[index], 2)
            if not math.isclose(expense_difference, 0.00, abs_tol=1.00):
                we_square = False
                if expense_difference < 0:
                    summary += \
                        f"{people[index]} is owed " + \
                        f"${abs(expense_difference)}.\n"
                elif expense_difference > .02:
                    summary += \
                        f"{people[index]} owes ${abs(expense_difference)}.\n"
        if we_square:
            summary += "We_Square!"
        print(summary)
        return summary

    def get_modified_transactions(self) -> list[tuple[int, str, str, str, str]]:
        transactions = self.retrieve_transactions()
        modified_transactions = []
        for transaction in transactions:
            if transaction["item_edited"]:
                transaction["item"] += "*"
            if transaction["amount_edited"]:
                transaction["amount"] += "*"
            if transaction["date_edited"]:
                transaction["date"] += "*"
            if transaction["paid_by_edited"]:
                transaction["paid_by"] += "*"
            if transaction["deleted"]:
                transaction["item"] = "(X)" + transaction["item"]
            modified_transactions.append((
                transaction["transaction_id"],
                transaction["item"],
                transaction["amount"],
                transaction["date"],
                transaction["paid_by"]))
        return modified_transactions

    def convert_people_data_for_json(self) -> list[dict]:
        people_data = self.retrieve_people_name_and_email()
        people = []
        for person_data in people_data:
            people.append(
                {
                    "name": person_data[0],
                    "email": person_data[1]
                }
            )
        return people

    def convert_transactions_for_json(self) -> list[dict]:
        transaction_data = self.get_modified_transactions()
        transactions = []
        for transaction in transaction_data:
            transactions.append(
                {
                "item": transaction[1],
                "amount": transaction[2],
                "date": transaction[3],
                "paid_by": transaction[4],
            })
        return transactions

    @staticmethod
    def call_template_service(ledger_json):
        # socket connection
        HOST = 'localhost'
        PORT = 65432
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((HOST, PORT))
        print(f"Connected to server: {HOST}:{PORT}...")
        print(f"\tSending Ledger to server.")
        client_socket.send(ledger_json.encode())
        print("\tSent Ledger to server successfully.")

        # receive html template
        html_doc = ''
        while True:
            print("Receiving...")
            response = client_socket.recv(1024).decode()
            html_doc += response

            if not response:
                print(f'HTML received from server: {html_doc} \n')
                client_socket.close()
                break

        return html_doc

    def send_ledger(self):

        ledger_data = {
            "ledger": {
                "title": self.retrieve_title_from_ledger_id(),
                "date": str(datetime.date.today()),
                "people": self.convert_people_data_for_json(),
                "summary": self.make_summary(),
                "transactions": self.convert_transactions_for_json()
            }
        }
        ledger_json = json.dumps(obj=ledger_data, indent=4)

        print(ledger_json)
        with open("new_sample.json", "w") as output:
            output.write(ledger_json)

        # html_doc = self.call_template_service(ledger_json)
        #
        # with open("email.html", "w") as output:
        #     output.write(html_doc)
