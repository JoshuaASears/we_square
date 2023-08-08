
from desktop.data.db_connection import DBConnection
import desktop.data.db_operations as db_operations

class AppModel:

    def __init__(self):
        self._db_connection = DBConnection()
        self._current_ledger = None
        self._transaction_being_updated = None

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    #
    #           GETTERS AND SETTERS
    #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def get_current_ledger(self):
        return self._current_ledger

    def set_ledger_from_title(self, title):
        ledger_id = db_operations.retrieve_lId_from_title(
            cursor=self._db_connection.get_cursor(),
            title=title
        )
        self.set_current_ledger(ledger_id)

    def set_transaction_being_updated(self, transaction):
        self._transaction_being_updated = transaction

    def set_current_ledger(self, ledger_id):
        self._current_ledger = ledger_id

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    #
    #           CREATE
    #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def create_and_set_ledger(self, title, people):
        ledger_id = db_operations.create_ledger(
            db_connection=self._db_connection,
            title=title,
            people=people
        )
        self.set_current_ledger(ledger_id)

    def create_or_update_transaction(self, values):
        if self._transaction_being_updated:
            self.update_transaction(values)
            self._transaction_being_updated = None
            return True
        else:
            db_operations.create_transaction(
                db_connection=self._db_connection,
                ledger_id=self._current_ledger,
                values=values
            )

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    #
    #           RETRIEVE
    #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def retrieve_ledgers_list(self):
        ledger_list = db_operations.retrieve_ledgers_list(
            cursor=self._db_connection.get_cursor()
        )
        return ledger_list

    def retrieve_lId_from_title(self, title):
        ledger_id = db_operations.retrieve_lId_from_title(
            cursor=self._db_connection.get_cursor(),
            title=title,
        )
        return ledger_id

    def retrieve_title_from_lId(self):
        title = db_operations.retrieve_title_from_lId(
            cursor=self._db_connection.get_cursor(),
            ledger_id=self._current_ledger
        )
        return title

    def retrieve_people_on_ledger(self):
        people = db_operations.retrieve_people_on_ledger(
            cursor=self._db_connection.get_cursor(),
            ledger_id=self._current_ledger
        )
        return people

    def retrieve_transactions(self):
        transactions = db_operations.retrieve_transactions(
            cursor=self._db_connection.get_cursor(),
            ledger_id=self._current_ledger
        )
        return transactions

    def retrieve_and_store_transaction_values(self, transaction_id):
        transaction = db_operations.retrieve_transaction_from_tId(
            cursor=self._db_connection.get_cursor(),
            transaction_id=transaction_id
        )
        self._transaction_being_updated = transaction
        return transaction[1:]

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    #
    #           UPDATE
    #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def update_transaction(self, values):
        db_operations.update_transaction(
            db_connection=self._db_connection,
            transaction_id=self._transaction_being_updated[0],
            old_values=self._transaction_being_updated[1:],
            new_values=values,
        )

    def mark_transaction_deleted(self, transaction_id):
        db_operations.mark_transaction_deleted(
            db_connection=self._db_connection,
            transaction_id=transaction_id
        )
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    #
    #           DELETE
    #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def delete_ledger(self):
        db_operations.delete_ledger(
            db_connection=self._db_connection,
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
        summary = ""
        return summary

    def send_ledger():
        title = model.retrieve_title_for_json(self.app.current_ledger)
        summary = model.retrieve_summary_for_json(self.app.current_ledger)
        persons = model.retrieve_persons_for_json(self.app.current_ledger)
        ledger = model.retrieve_transactions_for_json(self.app.current_ledger)
        date = {"date": str(dt.date.today())}

        ledger_data = {"ledger": [title, summary, persons, ledger, date]}

        data = json.dumps(obj=ledger_data, indent=4)

        with open("sample.json", "w") as outfile:
            outfile.write(data)