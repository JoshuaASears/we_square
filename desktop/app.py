
from desktop.model.app_model import AppModel
from desktop.views.select import Select
from desktop.views.create import Create
from desktop.views.ledger import Ledger

import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as tkm
import re


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self._app_model = AppModel()

        # configurations
        self.protocol("WM_DELETE_WINDOW", self.exit_handler)
        self.title("We_Square?")
        self.iconbitmap("resources/icon.ico")
        self.resizable(False, False)

        # top level frame to hold views
        self.view_window = ttk.Frame(
            self,
            padding='10',
        )
        self.view_window.pack()

        # set callbacks
        select_callbacks = [
            self.select_frame_raise_create_frame,
            self.select_frame_raise_ledger_frame
        ]
        create_callbacks = [
            self.raise_select_frame,
            self.create_frame_create_new_ledger
        ]
        ledger_callbacks = [
            self.ledger_frame_add_transaction,
            self.ledger_frame_edit_transaction,
            self.ledger_frame_delete_transaction,
            self.raise_select_frame,
            self.ledger_frame_send_ledger,
            self.ledger_frame_delete_ledger,
        ]

        # initialize views
        self.frames = {
            "select": Select(self.view_window, select_callbacks),
            "create": Create(self.view_window, create_callbacks),
            "ledger": Ledger(self.view_window, ledger_callbacks),
        }

        for frame in self.frames:
            self.frames[frame].grid(
                row=0,
                column=0,
                sticky="nsew"
            )

        # raise first view
        self.raise_frame("select")

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    #
    #           ROOT LEVEL FUNCTIONS
    #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    def exit_handler(self):
        self._app_model.close_connection()
        self.destroy()

    def raise_frame(self, frame):
        # for transitioning to select view: set available ledgers
        if frame == "select":
            self.select_frame_set_ledger_list()

        # for transitioning to ledger view: set all ledger data
        elif frame == "ledger":
            self.frames["ledger"].reset_fields(True, True, True)
            self.frames["ledger"].set_value_hints()
            self.ledger_set_title_and_people()
            self.ledger_set_transaction_and_summary()

        # raise view
        self.frames[frame].tkraise()

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    #
    #           CONTROL FUNCTIONS AND CALLBACKS FOR VIEWS
    #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    # # # 'select' VIEW FUNCTIONS
    def select_frame_set_ledger_list(self):
        ledger_list = self._app_model.retrieve_ledgers_list()
        if len(ledger_list) == 0:
            self.frames["select"].disable_ledger_select()
        else:
            self.frames["select"].set_ledger_list(ledger_list)

    # # # 'select' VIEW CALLBACKS
    def select_frame_raise_create_frame(self):
        self.raise_frame("create")

    def select_frame_raise_ledger_frame(self):
        title = self.frames["select"].get_selected_ledger()
        self._app_model.set_ledger_from_title(title)
        self.raise_frame("ledger")

    # # # 'create' and 'ledger' VIEW CALLBACKS

    def raise_select_frame(self):
        self.raise_frame("select")

    # # # 'create' VIEW CALL BACKS
    def create_frame_create_new_ledger(self):
        # validate title length
        title = self.frames["create"].get_title()
        if not 0 < len(title) < 16:
            tkm.showinfo(
                title="Unable to Create Ledger",
                message=f'Title must be between 1 and 15 characters, inclusive.',
                icon=tkm.INFO
            )
            return

        # validate title uniqueness
        ledger_id = self._app_model.retrieve_ledger_id_from_title(title)
        if ledger_id:
            tkm.showinfo(
                title="Unable to Create Ledger",
                message=f'Title "{title}" already in use.'
                        f'\nTitle must be unique',
                icon=tkm.INFO
            )
            return

        # validate quantity of people
        people = self.frames["create"].get_people()
        if len(people) < 2:
            tkm.showinfo(
                title="Unable to Create Ledger",
                message="Ledger must have 2 or more people to create.",
                icon=tkm.INFO
            )
            return

        # create new ledger and change frame
        self._app_model.create_and_set_ledger(title, people)
        self.frames["create"].reset_fields(True, True)
        self.raise_frame("ledger")

    # # # 'ledger' VIEW FUNCTIONS
    def ledger_set_transaction_and_summary(self):
        transactions = self._app_model.get_modified_transactions()
        self.frames["ledger"].set_transactions(transactions)
        summary = self._app_model.make_summary()
        self.frames["ledger"].set_summary(summary)

    def ledger_set_title_and_people(self):
        title = self._app_model.retrieve_title_from_ledger_id()
        self.frames["ledger"].set_title(title)
        people = self._app_model.retrieve_names_on_ledger()
        self.frames["ledger"].set_people(people)

    @staticmethod
    def validate_transaction_values(values):
        # 'item'
        if not 0 < len(values[0]) < 11:
            return "Item must be between 1 and 10 characters, inclusive."
        # 'amount'
        if not re.match('^\d*\.\d{1,2}$', values[1]) and \
                not re.match('^\d+$', values[1]):
            return "Amount must contain only integers or a single decimal."
        # 'date'
        if not re.match('^\d{4}-\d{2}-\d{2}$', values[2]):
            return "Date must be formatted: YYYY-MM-DD."
        return None

    # # # 'ledger' VIEW CALLBACKS
    def ledger_frame_add_transaction(self):
        values = self.frames["ledger"].get_new_transaction_values()
        invalidation_message = self.validate_transaction_values(values)
        if invalidation_message:
            tkm.showinfo(
                title="Invalid transaction record",
                message=f'{invalidation_message}',
                icon=tkm.INFO
            )
        else:
            self.frames["ledger"].reset_fields(
                item_amount_and_date=True,
                ledger_list=True
            )
            restore_state = self._app_model.create_or_update_transaction(
                values)
            if restore_state:
                self.frames["ledger"].restore_state()
            self.ledger_set_transaction_and_summary()

    def ledger_frame_edit_transaction(self):
        if self.frames["ledger"].is_transaction_selected():
            self.frames["ledger"].reset_fields(item_amount_and_date=True)
            transaction_id = \
                self.frames["ledger"].get_selected_transaction_id()
            values = self._app_model.retrieve_and_store_transaction_values(
                transaction_id=transaction_id
            )
            self.frames["ledger"].set_item_values(
                transaction_values=values
            )
            self.frames["ledger"].limit_state()

    def ledger_frame_delete_transaction(self):
        if self.frames["ledger"].is_transaction_selected():
            transaction_id = \
                self.frames["ledger"].get_selected_transaction_id()
            self._app_model.mark_transaction_deleted(transaction_id)
            self.frames["ledger"].reset_fields(ledger_list=True)
            self.ledger_set_transaction_and_summary()

    def ledger_frame_send_ledger(self):
        confirmation = tkm.askyesno(
            title="Confirmation: Email Ledger",
            message="Click Yes to email Ledger and Balance Summary to all "
                    "persons on this Ledger.",
            icon=tkm.INFO
        )
        if confirmation:
            self._app_model.send_ledger()

    def ledger_frame_delete_ledger(self):
        confirmation = tkm.askokcancel(
            title="Confirmation: Delete Ledger",
            message="Click OK to permanently delete this Ledger.",
            icon=tkm.WARNING
        )
        if confirmation:
            self._app_model.delete_ledger()
            self.raise_select_frame()


if __name__ == "__main__":
    app = App()
    app.mainloop()
