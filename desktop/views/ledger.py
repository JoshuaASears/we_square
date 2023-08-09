
import datetime
import tkinter as tk
import tkinter.font as tkf
import tkinter.ttk as ttk


width = 10


class Ledger(ttk.Frame):

    def __init__(self, frame, callbacks):
        super().__init__(frame)
        # intermediate variables for ui table
        self._selected_item = tk.StringVar()
        self._selected_paid_by = tk.StringVar(self)

        # widget definitions
        self._header_label = ttk.Label(
            self,
            text="[LEDGER TITLE]",
            font=tkf.Font(
                size=16,
                weight="bold"
            ),

        )
        self._names_label = ttk.Label(
            self,
            text="Shared by:"
        )
        self._names_list = ttk.Label(
            self,
            text="[NAMES ON LEDGER]"
        )
        self._item_label = ttk.Label(
            self,
            text="Item"
        )
        self._amount_label = ttk.Label(
            self,
            text="Amount"
        )
        self._date_label = ttk.Label(
            self,
            text="Date"
        )
        self._paid_by_label = ttk.Label(
            self,
            text="Paid By"
        )
        self._item_dropdown = ttk.Combobox(
            self,
            textvariable=self._selected_item,
            width=width
        )
        self._amount_entry = ttk.Entry(
            self,
            width=width
        )
        self._date_entry = ttk.Entry(
            self,
            width=width
        )
        self._paid_by_dropdown = ttk.OptionMenu(
            self,
            variable=self._selected_paid_by
        )
        self._paid_by_dropdown.config(width=width)
        columns = ('transaction_id', 'item', 'amount', 'date', 'paid_by')
        self._transactions = ttk.Treeview(
            self,
            columns=columns,
            show='',
            height=3,
        )
        self._transactions["displaycolumns"] = columns[1:]
        for index, column in enumerate(columns):
            self._transactions.column(
                index,
                width=width,
                anchor=tk.E
            )
        self._add_item_button = ttk.Button(
            self,
            text="add",
            command=callbacks[0],
            width=int(width/2)
        )
        self._edit_item_button = ttk.Button(
            self,
            text="edit",
            command=callbacks[1],
            width=int(width/2)
        )
        self._delete_item_button = ttk.Button(
            self,
            text="del",
            command=callbacks[2],
            width=int(width/2)
        )
        self._summary_label = ttk.Label(
            self,
            text="\n",
        )
        self._select_button = ttk.Button(
            self,
            text="Select Ledger",
            command=callbacks[3]
        )
        self._send_button = ttk.Button(
            self,
            text="Send Ledger",
            command=callbacks[4]
        )
        self._delete_ledger_button = ttk.Button(
            self,
            text="Delete Ledger",
            command=callbacks[5]
        )

        # configure grid rows
        for num in range(8):
            self.grid_rowconfigure(num, weight=1)
        # configure grid columns
        for num in range(5):
            self.grid_columnconfigure(num, weight=1)

        # frame layout
        self._header_label.grid(
            column=0,
            row=0,
            columnspan=4,
            sticky="WE"
        )
        self._names_label.grid(
            column=0,
            row=1,
            columnspan=1,
            sticky="W"
        )
        self._names_list.grid(
            column=1,
            row=1,
            columnspan=3,
            sticky="W"
        )
        self._item_label.grid(
            column=0,
            row=2,
            columnspan=1,
            sticky="W"
        )
        self._amount_label.grid(
            column=1,
            row=2,
            columnspan=1,
            sticky="W"
        )
        self._date_label.grid(
            column=2,
            row=2,
            columnspan=1,
            sticky="W"
        )
        self._paid_by_label.grid(
            column=3,
            row=2,
            columnspan=1,
            sticky="W"
        )
        self._item_dropdown.grid(
            column=0,
            row=3,
            columnspan=1,
            sticky="WE"
        )
        self._amount_entry.grid(
            column=1,
            row=3,
            columnspan=1,
            sticky="WE"
        )
        self._date_entry.grid(
            column=2,
            row=3,
            columnspan=1,
            sticky="WE"
        )
        self._paid_by_dropdown.grid(
            column=3,
            row=3,
            columnspan=1,
            sticky="WE"
        )
        self._transactions.grid(
            column=0,
            row=4,
            columnspan=4,
            rowspan=2,
            sticky="NSEW"
        )
        self._add_item_button.grid(
            column=4,
            row=3,
            columnspan=1,
            sticky="NS"
        )
        self._edit_item_button.grid(
            column=4,
            row=4,
            columnspan=1,
            rowspan=1,
            sticky="NS"
        )
        self._delete_item_button.grid(
            column=4,
            row=5,
            columnspan=1,
            rowspan=1,
            sticky="NS"
        )
        self._summary_label.grid(
            column=0,
            row=6,
            columnspan=5,
            sticky="W"
        )
        self._select_button.grid(
            column=0,
            row=7,
            columnspan=1,
            sticky="WE"
        )
        self._send_button.grid(
            column=1,
            row=7,
            columnspan=1,
            sticky="WE"
        )
        self._delete_ledger_button.grid(
            column=2,
            row=7,
            columnspan=1,
            sticky="WE"
        )

    def get_new_transaction_values(self):
        item = self._item_dropdown.get().strip()
        amount = self._amount_entry.get().strip()
        date = self._date_entry.get().strip()
        paid_by = self._selected_paid_by.get().strip()
        return item, amount, date, paid_by

    def get_selected_transaction_id(self):
        row = self._transactions.selection()[0]
        transaction_id = self._transactions.item(row)['values'][0]
        return transaction_id

    def set_item_values(self, transaction_values):
        self._item_dropdown.insert(0, transaction_values[0])
        self._amount_entry.insert(0, transaction_values[1])
        self._date_entry.insert(0, transaction_values[2])
        self._selected_paid_by.set(transaction_values[3])

    def set_people(self, people):
        for index, person in enumerate(people):
            if index == 0:
                self._names_list['text'] = person
            else:
                self._names_list['text'] += ", " + person
            self._paid_by_dropdown['menu'].add_command(
                label=person,
                command=tk._setit(self._selected_paid_by, person)
            )
        self._item_dropdown['values'] = people
        self._selected_paid_by.set(people[0])

    def set_summary(self, summary):
        self._summary_label['text'] = summary

    def set_value_hints(self):
        self._amount_entry.insert(0, "0.00")
        self._date_entry.insert(0, str(datetime.date.today()))

    def set_title(self, title):
        self._header_label['text'] = title

    def set_transactions(self, transactions):
        for transaction in transactions:
            self._transactions.insert('', tk.END, values=transaction)

    def reset_fields(self, 
            item_amount_and_date=False, paid_by=False, ledger_list=False):
        if item_amount_and_date:
            self._item_dropdown.delete(0, tk.END)
            self._amount_entry.delete(0, tk.END)
            self._date_entry.delete(0, tk.END)
        if paid_by:
            self._paid_by_dropdown['menu'].delete(0, tk.END)
        if ledger_list:
            for index in self._transactions.get_children():
                self._transactions.delete(index)

    def limit_state(self):
        self._add_item_button['text'] = "upd"
        self._edit_item_button["state"] = tk.DISABLED
        self._delete_item_button["state"] = tk.DISABLED
        self._select_button["state"] = tk.DISABLED
        self._send_button["state"] = tk.DISABLED
        self._delete_ledger_button["state"] = tk.DISABLED

    def restore_state(self):
        self._add_item_button['text'] = "add"
        self._edit_item_button["state"] = tk.NORMAL
        self._delete_item_button["state"] = tk.NORMAL
        self._select_button["state"] = tk.NORMAL
        self._send_button["state"] = tk.NORMAL
        self._delete_ledger_button["state"] = tk.NORMAL

    def is_transaction_selected(self):
        if self._transactions.selection():
            return True
