import tkinter as tk
import tkinter.ttk as ttk


class Ledger(tk.Frame):

    def __init__(
            self,
            app,
            frame,
            nav_font
    ):
        super().__init__(frame)
        self.app = app

        # configure grid weight
        # self.grid_rowconfigure(0, weight=1)
        # self.grid_rowconfigure(1, weight=1)
        # self.grid_columnconfigure(0, weight=1)
        # self.grid_columnconfigure(1, weight=1)

        # widget definitions
        header_label = tk.Label(
            master=self,
            text="[LEDGER TITLE]"
        )
        shared_by_label = tk.Label(
            master=self,
            text="Shared by:"
        )
        shared_by_list = tk.Label(
            master=self,
            text="[NAMES ON LEDGER]"
        )
        transaction_label = tk.Label(
            master=self,
            text="Transaction"
        )
        amount_label = tk.Label(
            master=self,
            text="Amount"
        )
        paid_by_label = tk.Label(
            master=self,
            text="Paid By"
        )
        date_label = tk.Label(
            master=self,
            text="Date"
        )
        ledger_label = tk.Label(
            master=self,
            text="[ITEMS ON LEDGER]"
        )
        transaction_entry = tk.Entry(
            master=self,
        )
        amount_entry = tk.Entry(
            master=self,
            width=10
        )
        paid_by_entry = tk.Entry(
            master=self,
            width=10
        )
        date_entry = tk.Entry(
            master=self,
            width=10
        )
        add_button = tk.Button(
            master=self,
            text="+",
            command=self.add_item
        )
        select_button = tk.Button(
            master=self,
            text="Select Ledger",
            font=nav_font,
            command=self.raise_select_frame
        )
        total_button = tk.Button(
            master=self,
            text="We_Square?",
            font=nav_font,
            command=self.raise_total_frame
        )

        # frame layout
        header_label.grid(
            column=0,
            row=0,
        )
        shared_by_label.grid(
            column=0,
            row=1
        )
        shared_by_list.grid(
            column=1,
            row=1
        )
        transaction_label.grid(
            column=0,
            row=2,
        )
        amount_label.grid(
            column=1,
            row=2,
        )
        paid_by_label.grid(
            column=2,
            row=2,
        )
        date_label.grid(
            column=3,
            row=2,
        )
        ledger_label.grid(
            column=0,
            row=3,
        )
        transaction_entry.grid(
            column=0,
            row=4,
        )
        amount_entry.grid(
            column=1,
            row=4,
        )
        paid_by_entry.grid(
            column=2,
            row=4,
        )
        date_entry.grid(
            column=3,
            row=4,
        )
        add_button.grid(
            column=4,
            row=4,
        )
        select_button.grid(
            column=0,
            row=5,
            columnspan=1,
            sticky="EW",
        )
        total_button.grid(
            column=1,
            row=5,
            columnspan=1,
            sticky="EW",
        )

    def raise_select_frame(self):
        self.app.raise_frame("select")

    def raise_total_frame(self):
        self.app.raise_frame("total")

    def add_item(self):
        pass
