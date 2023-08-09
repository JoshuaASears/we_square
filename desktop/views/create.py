
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as tkm

width = 10


class Create(ttk.Frame):

    def __init__(self, frame, callbacks):
        super().__init__(frame)
        # widget definitions
        self._title_label = ttk.Label(
            self,
            text="Ledger Title",
        )
        self._title_entry = ttk.Entry(
            self,
        )
        self._name_label = ttk.Label(
            self,
            text="Name"
        )
        self._email_label = ttk.Label(
            self,
            text="Email"
        )
        self._name_entry = ttk.Entry(
            self,
        )
        self._email_entry = ttk.Entry(
            self,
        )
        self._add_button = ttk.Button(
            self,
            text="add",
            command=self.add_person,
            width=int(width / 2),
        )
        self._name_list = ttk.Treeview(
            self,
            columns=('name', 'email'),
            show='',
            height=3,
        )
        self._edit_button = ttk.Button(
            self,
            text="edit",
            command=self.edit_person,
            width=int(width / 2)
        )
        self._delete_button = ttk.Button(
            self,
            text="del",
            command=self.delete_person,
            width=int(width / 2)
        )
        self._select_button = ttk.Button(
            self,
            text="Back",
            command=callbacks[0]
        )
        self._ledger_button = ttk.Button(
            self,
            text="Create Ledger",
            command=callbacks[1],
        )

        # configure grid rows
        for num in range(8):
            self.grid_rowconfigure(num, weight=1)
        # configure grid columns
        for num in range(3):
            self.grid_columnconfigure(num, weight=1)

        # frame layout

        self._title_label.grid(
            column=0,
            row=0,
            columnspan=1,
            sticky="W"
        )
        self._title_entry.grid(
            column=0,
            row=1,
            columnspan=2,
            sticky="EW"
        )
        self._name_label.grid(
            column=0,
            row=2,
            columnspan=1,
            sticky="EW"
        )
        self._email_label.grid(
            column=1,
            row=2,
            columnspan=1,
            sticky="EW"
        )
        self._name_entry.grid(
            column=0,
            row=3,
            columnspan=1,
            sticky="EW"
        )
        self._email_entry.grid(
            column=1,
            row=3,
            columnspan=1,
            sticky="EW"
        )
        self._add_button.grid(
            column=2,
            row=3,
            columnspan=1,
            sticky="NS"
        )
        self._name_list.grid(
            column=0,
            row=4,
            columnspan=2,
            rowspan=2,
            sticky="NSEW"
        )
        self._edit_button.grid(
            column=2,
            row=4,
            columnspan=1,
            sticky="NS"
        )
        self._delete_button.grid(
            column=2,
            row=5,
            columnspan=1,
            sticky="NS"
        )
        self._select_button.grid(
            column=0,
            row=6,
            columnspan=1,
            sticky="EW"
        )
        self._ledger_button.grid(
            column=1,
            row=6,
            columnspan=1,
            sticky="EW"
        )

    def get_people(self):
        people = []
        for row in self._name_list.get_children():
            name = self._name_list.item(row)['values'][0].strip()
            email = self._name_list.item(row)['values'][1].strip()
            people.append((name, email))
        return people

    def get_title(self):
        return self._title_entry.get().strip()

    def reset_fields(self, name_and_email=False, title_and_list=False):
        if name_and_email:
            self._name_entry.delete(0, tk.END)
            self._email_entry.delete(0, tk.END)
        if title_and_list:
            self._title_entry.delete(0, tk.END)
            for index in self._name_list.get_children():
                self._name_list.delete(index)

    def add_person(self):
        # get string data from fields and add
        name = self._name_entry.get()
        email = self._email_entry.get()
        if not 0 < len(name) < 16:
            tkm.showinfo(
                title="Unable to add person",
                message="Name must be between 1 and 15 characters, inclusive.",
                icon=tkm.INFO
            )
            return
        if not 5 < len(email) < 30:
            tkm.showinfo(
                title="Unable to add person",
                message="Please enter valid email.",
                icon=tkm.INFO
            )
            return
        self._name_list.insert('', tk.END, values=(name, email))

        # clear old string data from fields
        self._name_entry.delete(0, tk.END)
        self._email_entry.delete(0, tk.END)

    def edit_person(self):
        if self._name_list.selection():
            self.reset_fields(name_and_email=True)
            row = self._name_list.selection()[0]
            name = self._name_list.item(row)['values'][0]
            email = self._name_list.item(row)['values'][1]
            self._name_entry.insert(0, name)
            self._email_entry.insert(0, email)
            self._name_list.delete(row)

    def delete_person(self):
        if self._name_list.selection():
            row = self._name_list.selection()[0]
            self._name_list.delete(row)
