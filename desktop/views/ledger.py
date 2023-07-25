import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as tkm
import desktop.model.db_ledger as model


width = 10


class Ledger(ttk.Frame):

    def __init__(
            self,
            app,
            frame,
    ):
        super().__init__(frame)
        self.app = app
        # temp variables
        self.ledger = None
        self.item_index = None
        self.selected_item = tk.StringVar()
        self.selected_paid_by = tk.StringVar()

        # widget definitions
        self.header_label = ttk.Label(
            self,
            text="[LEDGER TITLE]"
        )
        self.shared_by_label = ttk.Label(
            self,
            text="Shared by:"
        )
        self.shared_by_list = ttk.Label(
            self,
            text="[NAMES ON LEDGER]"
        )
        self.item_label = ttk.Label(
            self,
            text="Item"
        )
        self.amount_label = ttk.Label(
            self,
            text="Amount"
        )
        self.date_label = ttk.Label(
            self,
            text="Date"
        )
        self.paid_by_label = ttk.Label(
            self,
            text="Paid By"
        )
        self.item_dropdown = ttk.Combobox(
            self,
            textvariable=self.selected_item,
            width=width
        )
        self.amount_entry = ttk.Entry(
            self,
            width=width
        )
        self.date_entry = ttk.Entry(
            self,
            width=width
        )
        self.paid_by_dropdown = ttk.Combobox(
            self,
            textvariable=self.selected_paid_by,
            width=width
        )

        columns = ('item', 'amount', 'date', 'paid_by')
        self.ledger_list = ttk.Treeview(
            self,
            columns=columns,
            show='',
            height=3,
        )
        for index, column in enumerate(columns):
            self.ledger_list.column(index, width=width)

        self.add_item_button = ttk.Button(
            self,
            text="add",
            command=self.add_item,
            width=int(width/2)
        )
        self.edit_item_button = ttk.Button(
            self,
            text="edit",
            command=self.edit_item,
            width=int(width/2)
        )
        self.delete_item_button = ttk.Button(
            self,
            text="del",
            command=self.delete_item,
            width=int(width/2)
        )
        self.summary_label = ttk.Label(
            self,
            text="[LEDGER SUMMARY]",
        )
        self.select_button = ttk.Button(
            self,
            text="Select Ledger",
            command=self.raise_select_frame
        )
        self.send_button = ttk.Button(
            self,
            text="Send Ledger",
            command=self.send_ledger
        )
        self.delete_ledger_button = ttk.Button(
            self,
            text="Delete Ledger",
            command=self.delete_ledger
        )

        # configure grid rows
        for num in range(8):
            self.grid_rowconfigure(num, weight=1)
        # configure grid columns
        for num in range(5):
            self.grid_columnconfigure(num, weight=1)

        # frame layout
        self.header_label.grid(
            column=0,
            row=0,
            columnspan=4,
            sticky="WE"
        )
        self.shared_by_label.grid(
            column=0,
            row=1,
            columnspan=1,
            sticky="W"
        )
        self.shared_by_list.grid(
            column=1,
            row=1,
            columnspan=3,
            sticky="W"
        )
        self.item_label.grid(
            column=0,
            row=2,
            columnspan=1,
            sticky="W"
        )
        self.amount_label.grid(
            column=1,
            row=2,
            columnspan=1,
            sticky="W"
        )
        self.date_label.grid(
            column=2,
            row=2,
            columnspan=1,
            sticky="W"
        )
        self.paid_by_label.grid(
            column=3,
            row=2,
            columnspan=1,
            sticky="W"
        )
        self.item_dropdown.grid(
            column=0,
            row=3,
            columnspan=1,
            sticky="WE"
        )
        self.amount_entry.grid(
            column=1,
            row=3,
            columnspan=1,
            sticky="WE"
        )
        self.date_entry.grid(
            column=2,
            row=3,
            columnspan=1,
            sticky="WE"
        )
        self.paid_by_dropdown.grid(
            column=3,
            row=3,
            columnspan=1,
            sticky="WE"
        )
        self.ledger_list.grid(
            column=0,
            row=4,
            columnspan=4,
            rowspan=2,
            sticky="NSEW"
        )
        self.add_item_button.grid(
            column=4,
            row=3,
            columnspan=1,
            sticky="NS"
        )
        self.edit_item_button.grid(
            column=4,
            row=4,
            columnspan=1,
            rowspan=1,
            sticky="NS"
        )
        self.delete_item_button.grid(
            column=4,
            row=5,
            columnspan=1,
            rowspan=1,
            sticky="NS"
        )
        self.summary_label.grid(
            column=0,
            row=6,
            columnspan=5,
            sticky="W"
        )
        self.select_button.grid(
            column=0,
            row=7,
            columnspan=1,
            sticky="WE"
        )
        self.send_button.grid(
            column=1,
            row=7,
            columnspan=1,
            sticky="WE"
        )
        self.delete_ledger_button.grid(
            column=2,
            row=7,
            columnspan=1,
            sticky="WE"
        )

    def update(
            self,
            title=False,
            persons=False,
            ledger_list=False,
            summary=False
    ):

        # set title
        if title:
            title = model.retrieve_title(self.ledger)
            self.header_label['text'] = title

        # set persons
        if persons:
            person_list = model.retrieve_persons(self.ledger)
            # label, drop down, menu buttons
            for index, person in enumerate(person_list):
                if index == 0:
                    self.shared_by_list['text'] = person
                else:
                    self.shared_by_list['text'] += ", " + person
            self.item_dropdown['values'] = person_list
            self.paid_by_dropdown['values'] = person_list

        # set items
        if ledger_list:
            item_list = model.retrieve_transactions(self.ledger)
            for item in item_list:
                self.ledger_list.insert('', tk.END, values=item)

        # set summary
        if summary:
            pass
    
    def reset_fields(
            self,
            item_dropdown=False,
            amount_entry=False,
            date_entry=False,
            paid_by_dropdown=False,
            ledger_list=False
    ):
        if item_dropdown:
            self.item_dropdown.delete(0, tk.END)
        if amount_entry:
            self.amount_entry.delete(0, tk.END)
        if date_entry:
            self.date_entry.delete(0, tk.END)
        if paid_by_dropdown:
            self.paid_by_dropdown.delete(0, tk.END)
        if ledger_list:
            for index in self.ledger_list.get_children():
                self.ledger_list.delete(index)

    def add_item(self):
        item = self.item_dropdown.get()
        amount = self.amount_entry.get()
        date = self.date_entry.get()
        paid_by = self.paid_by_dropdown.get()

        model.add_transaction(
            ledger=self.ledger,
            item=item,
            amount=amount,
            date=date,
            paid_by=paid_by,
            key=self.item_index
        )
        self.reset_fields(
            item_dropdown=True,
            amount_entry=True,
            date_entry=True,
            paid_by_dropdown=True,
            ledger_list=True
        )
        self.update(
            ledger_list=True,
            summary=True
        )

        # restore ui state from step 2 of edit
        if self.item_index:
            self.add_item_button['text'] = "add"
            self.edit_item_button["state"] = tk.NORMAL
            self.delete_item_button["state"] = tk.NORMAL
            self.select_button["state"] = tk.NORMAL
            self.send_button["state"] = tk.NORMAL
            self.delete_ledger_button["state"] = tk.NORMAL
            self.item_index = None

    def edit_item(self):
        if self.ledger_list.selection():
            index = int(self.ledger_list.selection()[0][1:])
            self.item_index = index
            self.reset_fields(
                item_dropdown=True,
                amount_entry=True,
                date_entry=True,
                paid_by_dropdown=True,
            )
            row = self.ledger_list.selection()[0]
            item = self.ledger_list.item(row)['values'][0]
            amount = self.ledger_list.item(row)['values'][1]
            date = self.ledger_list.item(row)['values'][2]
            paid_by = self.ledger_list.item(row)['values'][3]
            self.item_dropdown.insert(0, item)
            self.amount_entry.insert(0, amount)
            self.date_entry.insert(0, date)
            self.paid_by_dropdown.insert(0, paid_by)

            # set ui state for to force step 2 of edit via add
            self.add_item_button['text'] = "upd"
            self.edit_item_button["state"] = tk.DISABLED
            self.delete_item_button["state"] = tk.DISABLED
            self.select_button["state"] = tk.DISABLED
            self.send_button["state"] = tk.DISABLED
            self.delete_ledger_button["state"] = tk.DISABLED

    def delete_item(self):
        if self.ledger_list.selection():
            index = int(self.ledger_list.selection()[0][1:])
            model.delete_transaction(self.ledger, index)

    def raise_select_frame(self):
        self.app.raise_frame("select")

    def send_ledger(self):
        confirmation = tkm.askyesno(
            title="Confirmation: Email Ledger",
            message="Click Yes to email Ledger and Balance Summary to all "
                    "persons on this Ledger.",
            icon=tkm.INFO
        )
        if confirmation:
            #TODO: email
            pass

    def delete_ledger(self):
        confirmation = tkm.askokcancel(
            title="Confirmation: Delete Ledger",
            message="Click OK to permanently delete this Ledger.",
            icon=tkm.WARNING
        )
        if confirmation:
            self.app.ledgers.remove(self.ledger)
            self.raise_select_frame()
