import tkinter as tk


class Create(tk.Frame):

    def __init__(
            self,
            app,
            frame,
            nav_font
    ):
        super().__init__(frame)
        self.app = app

        # configure grid weight
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # widget definitions
        header_label = tk.Label(
            master=self,
            text="New Ledger"
        )
        title_label = tk.Label(
            master=self,
            text="Ledger Title"
        )
        title_entry = tk.Entry(
            master=self,
        )
        name_label = tk.Label(
            master=self,
            text="Name"
        )
        email_label = tk.Label(
            master=self,
            text="Email"
        )
        name_list = tk.Label(
            master=self,
            text="[NAMES/EMAILS ON LEDGER]"
        )
        name_entry = tk.Entry(
            master=self,
        )
        email_entry = tk.Entry(
            master=self,
        )
        add_button = tk.Button(
            master=self,
            text="+",
            command=self.add_person
        )
        home_button = tk.Button(
            master=self,
            text="Home",
            font=nav_font,
            command=self.raise_home_frame
        )
        create_button = tk.Button(
            master=self,
            text="Create Ledger",
            font=nav_font,
            command=self.raise_ledger_frame
        )

        # frame layout
        header_label.grid(
            column=0,
            row=0,
            columnspan=2,
            sticky="EW"
        )
        title_label.grid(
            column=0,
            row=1,
            columnspan=1,
            sticky="W"
        )
        title_entry.grid(
            column=0,
            row=2,
            columnspan=2,
            sticky="EW"
        )
        name_label.grid(
            column=0,
            row=3,
            columnspan=1,
            sticky="W"
        )
        email_label.grid(
            column=1,
            row=3,
            columnspan=1,
            sticky="W"
        )
        name_list.grid(
            column=0,
            row=4,
            columnspan=2,
            sticky="EW"
        )
        name_entry.grid(
            column=0,
            row=5,
            columnspan=1,
            sticky="EW"
        )
        email_entry.grid(
            column=1,
            row=5,
            columnspan=1,
            sticky="EW"
        )
        add_button.grid(
            column=2,
            row=5,
            columnspan=1
        )
        home_button.grid(
            column=0,
            row=6,
            columnspan=1,
            sticky="EW",
        )
        create_button.grid(
            column=1,
            row=6,
            columnspan=1,
            sticky="EW",
        )

    def raise_home_frame(self):
        self.app.raise_frame("home")

    def raise_ledger_frame(self):
        self.app.raise_frame("ledger")

    def add_person(self):
        pass
