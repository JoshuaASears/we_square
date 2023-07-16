import tkinter.ttk as ttk

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
        title_label = ttk.Label(
            self,
            text="Ledger Title",
        )
        title_entry = ttk.Entry(
            self,
        )
        name_label = ttk.Label(
            self,
            text="Name"
        )
        email_label = ttk.Label(
            self,
            text="Email"
        )
        name_entry = ttk.Entry(
            self,
        )
        email_entry = ttk.Entry(
            self,
        )
        add_button = ttk.Button(
            self,
            text="add",
            command=self.add_person,
            width=int(width / 2),
        )
        name_list = ttk.Treeview(
            self,
            height=3,
            listvariable=None,
        )
        edit_button = ttk.Button(
            self,
            text="edit",
            command=self.edit_person,
            width=int(width / 2)
        )
        delete_button = ttk.Button(
            self,
            text="del",
            command=self.delete_person,
            width=int(width / 2)
        )
        select_button = ttk.Button(
            self,
            text="Back",
            command=self.raise_select_frame
        )
        ledger_button = ttk.Button(
            self,
            text="Create Ledger",
            command=self.raise_ledger_frame
        )

        # configure grid rows
        for num in range(8):
            self.grid_rowconfigure(num, weight=1)
        # configure grid columns
        for num in range(3):
            self.grid_columnconfigure(num, weight=1)

        # frame layout

        title_label.grid(
            column=0,
            row=0,
            columnspan=1,
            sticky="W"
        )
        title_entry.grid(
            column=0,
            row=1,
            columnspan=2,
            sticky="EW"
        )
        name_label.grid(
            column=0,
            row=2,
            columnspan=1,
            sticky="EW"
        )
        email_label.grid(
            column=1,
            row=2,
            columnspan=1,
            sticky="EW"
        )
        name_entry.grid(
            column=0,
            row=3,
            columnspan=1,
            sticky="EW"
        )
        email_entry.grid(
            column=1,
            row=3,
            columnspan=1,
            sticky="EW"
        )
        add_button.grid(
            column=2,
            row=3,
            columnspan=1,
            sticky="NS"
        )
        name_list.grid(
            column=0,
            row=4,
            columnspan=2,
            rowspan=2,
            sticky="NSEW"
        )
        edit_button.grid(
            column=2,
            row=4,
            columnspan=1,
            sticky="NS"
        )
        delete_button.grid(
            column=2,
            row=5,
            columnspan=1,
            sticky="NS"
        )
        select_button.grid(
            column=0,
            row=6,
            columnspan=1,
            sticky="EW"
        )
        ledger_button.grid(
            column=1,
            row=6,
            columnspan=1,
            sticky="EW"
        )

    def raise_select_frame(self):
        self.app.raise_frame("select")

    def raise_ledger_frame(self):
        self.app.raise_frame("ledger")

    def add_person(self):
        pass

    def edit_person(self):
        pass

    def delete_person(self):
        pass
