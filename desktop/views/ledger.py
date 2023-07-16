import tkinter.ttk as ttk
import tkinter.messagebox as tkm

width = 10


class Ledger(ttk.Frame):

    def __init__(
            self,
            app,
            frame,
    ):
        super().__init__(frame)
        self.app = app

        # widget definitions
        header_label = ttk.Label(
            self,
            text="[LEDGER TITLE]"
        )
        shared_by_label = ttk.Label(
            self,
            text="Shared by:"
        )
        shared_by_list = ttk.Label(
            self,
            text="[NAMES ON LEDGER]"
        )
        item_label = ttk.Label(
            self,
            text="Item"
        )
        amount_label = ttk.Label(
            self,
            text="Amount"
        )
        date_label = ttk.Label(
            self,
            text="Date"
        )
        paid_by_label = ttk.Label(
            self,
            text="Paid By"
        )
        item_dropdown = ttk.Combobox(
            self,
            width=width
        )
        amount_entry = ttk.Entry(
            self,
            width=width
        )
        date_entry = ttk.Entry(
            self,
            width=width
        )
        paid_by_menubutton = ttk.Menubutton(
            self,
            width=width
        )
        ledger_list = ttk.Treeview(
            self,
            height=3,
            listvariable=None
        )
        add_item_button = ttk.Button(
            self,
            text="add",
            command=self.add_item,
            width=int(width/2)
        )
        edit_item_button = ttk.Button(
            self,
            text="edit",
            command=self.edit_item,
            width=int(width/2)
        )
        delete_item_button = ttk.Button(
            self,
            text="del",
            command=self.delete_item,
            width=int(width/2)
        )
        summary_label = ttk.Label(
            self,
            text="[LEDGER SUMMARY]",
        )
        select_button = ttk.Button(
            self,
            text="Select Ledger",
            command=self.raise_select_frame
        )
        send_button = ttk.Button(
            self,
            text="Send Ledger",
            command=self.send_ledger
        )
        delete_ledger_button = ttk.Button(
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
        header_label.grid(
            column=0,
            row=0,
            columnspan=4,
            sticky="WE"
        )
        shared_by_label.grid(
            column=0,
            row=1,
            columnspan=1,
            sticky="W"
        )
        shared_by_list.grid(
            column=1,
            row=1,
            columnspan=3,
            sticky="W"
        )
        item_label.grid(
            column=0,
            row=2,
            columnspan=1,
            sticky="W"
        )
        amount_label.grid(
            column=1,
            row=2,
            columnspan=1,
            sticky="W"
        )
        date_label.grid(
            column=2,
            row=2,
            columnspan=1,
            sticky="W"
        )
        paid_by_label.grid(
            column=3,
            row=2,
            columnspan=1,
            sticky="W"
        )
        item_dropdown.grid(
            column=0,
            row=3,
            columnspan=1,
            sticky="WE"
        )
        amount_entry.grid(
            column=1,
            row=3,
            columnspan=1,
            sticky="WE"
        )
        date_entry.grid(
            column=2,
            row=3,
            columnspan=1,
            sticky="WE"
        )
        paid_by_menubutton.grid(
            column=3,
            row=3,
            columnspan=1,
            sticky="WE"
        )
        ledger_list.grid(
            column=0,
            row=4,
            columnspan=4,
            rowspan=2,
            sticky="NSEW"
        )
        add_item_button.grid(
            column=4,
            row=3,
            columnspan=1,
            sticky="NS"
        )
        edit_item_button.grid(
            column=4,
            row=4,
            columnspan=1,
            rowspan=1,
            sticky="NS"
        )
        delete_item_button.grid(
            column=4,
            row=5,
            columnspan=1,
            rowspan=1,
            sticky="NS"
        )
        summary_label.grid(
            column=0,
            row=6,
            columnspan=5,
            sticky="W"
        )
        select_button.grid(
            column=0,
            row=7,
            columnspan=1,
            sticky="WE"
        )
        send_button.grid(
            column=1,
            row=7,
            columnspan=1,
            sticky="WE"
        )
        delete_ledger_button.grid(
            column=2,
            row=7,
            columnspan=1,
            sticky="WE"
        )

    def raise_select_frame(self):
        self.app.raise_frame("select")

    def raise_home_frame(self):
        self.app.raise_frame("home")

    def add_item(self):
        pass

    def edit_item(self):
        pass

    def delete_item(self):
        pass

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
            #TODO: delete ledger tables
            pass
