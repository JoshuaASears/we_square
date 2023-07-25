import tkinter as tk
import tkinter.messagebox as tkm
import tkinter.ttk as ttk

import desktop.model.db_create as model

width = 10


class Create(ttk.Frame):

    def __init__(
            self,
            app,
            frame
    ):
        super().__init__(frame)
        self.app = app

        # widget definitions
        self.title_label = ttk.Label(
            self,
            text="Ledger Title",
        )
        self.title_entry = ttk.Entry(
            self,
        )
        self.name_label = ttk.Label(
            self,
            text="Name"
        )
        self.email_label = ttk.Label(
            self,
            text="Email"
        )
        self.name_entry = ttk.Entry(
            self,
        )
        self.email_entry = ttk.Entry(
            self,
        )
        self.add_button = ttk.Button(
            self,
            text="add",
            command=self.add_person,
            width=int(width / 2),
        )
        self.name_list = ttk.Treeview(
            self,
            columns=('name', 'email'),
            show='',
            height=3,
        )
        self.edit_button = ttk.Button(
            self,
            text="edit",
            command=self.edit_person,
            width=int(width / 2)
        )
        self.delete_button = ttk.Button(
            self,
            text="del",
            command=self.delete_person,
            width=int(width / 2)
        )
        self.select_button = ttk.Button(
            self,
            text="Back",
            command=self.raise_select_frame
        )
        self.ledger_button = ttk.Button(
            self,
            text="Create Ledger",
            command=self.raise_ledger_frame,
        )

        # configure grid rows
        for num in range(8):
            self.grid_rowconfigure(num, weight=1)
        # configure grid columns
        for num in range(3):
            self.grid_columnconfigure(num, weight=1)

        # frame layout

        self.title_label.grid(
            column=0,
            row=0,
            columnspan=1,
            sticky="W"
        )
        self.title_entry.grid(
            column=0,
            row=1,
            columnspan=2,
            sticky="EW"
        )
        self.name_label.grid(
            column=0,
            row=2,
            columnspan=1,
            sticky="EW"
        )
        self.email_label.grid(
            column=1,
            row=2,
            columnspan=1,
            sticky="EW"
        )
        self.name_entry.grid(
            column=0,
            row=3,
            columnspan=1,
            sticky="EW"
        )
        self.email_entry.grid(
            column=1,
            row=3,
            columnspan=1,
            sticky="EW"
        )
        self.add_button.grid(
            column=2,
            row=3,
            columnspan=1,
            sticky="NS"
        )
        self.name_list.grid(
            column=0,
            row=4,
            columnspan=2,
            rowspan=2,
            sticky="NSEW"
        )
        self.edit_button.grid(
            column=2,
            row=4,
            columnspan=1,
            sticky="NS"
        )
        self.delete_button.grid(
            column=2,
            row=5,
            columnspan=1,
            sticky="NS"
        )
        self.select_button.grid(
            column=0,
            row=6,
            columnspan=1,
            sticky="EW"
        )
        self.ledger_button.grid(
            column=1,
            row=6,
            columnspan=1,
            sticky="EW"
        )

    def reset_fields(
            self,
            title_entry=False,
            name_entry=False,
            email_entry=False,
            name_list=False
    ):
        if title_entry:
            self.title_entry.delete(0, tk.END)
        if name_entry:
            self.name_entry.delete(0, tk.END)
        if email_entry:
            self.email_entry.delete(0, tk.END)
        if name_list:
            for index in self.name_list.get_children():
                self.name_list.delete(index)

    def add_person(self):
        # get string data from fields and add
        name = self.name_entry.get()
        email = self.email_entry.get()
        self.name_list.insert('', tk.END, values=(name, email))

        # clear old string data from fields
        self.name_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)

    def edit_person(self):
        if self.name_list.selection():
            self.reset_fields(name_entry=True, email_entry=True)
            row = self.name_list.selection()[0]
            name = self.name_list.item(row)['values'][0]
            email = self.name_list.item(row)['values'][1]
            self.name_entry.insert(0, name)
            self.email_entry.insert(0, email)
            self.name_list.delete(row)

    def delete_person(self):
        if self.name_list.selection():
            row = self.name_list.selection()[0]
            self.name_list.delete(row)

    def raise_select_frame(self):
        self.app.raise_frame("select")

    def raise_ledger_frame(self):
        # initialize objects in data model
        persons = []
        for row in self.name_list.get_children():
            name = self.name_list.item(row)['values'][0]
            email = self.name_list.item(row)['values'][1]
            persons.append((name, email))

        # valid quantity of persons, continue
        if len(persons) >= 2:
            title = self.title_entry.get()
            ledger = model.create_ledger(title, persons)

            # reset fields
            self.reset_fields(True, True, True, True)

            # append ledger to app ledger collection
            self.app.ledgers.append(ledger)
            ledger_index = self.app.ledgers.index(ledger)

            # change frame with ledger object
            self.app.raise_frame("ledger", ledger_index)

        # invalid quantity of persons
        else:
            tkm.showinfo(
                title="Unable to Create Ledger",
                message="Ledger must have 2 or more persons to create.",
                icon=tkm.INFO
            )
