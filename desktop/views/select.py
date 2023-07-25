import tkinter as tk
import tkinter.font as tkf
import tkinter.ttk as ttk

import desktop.model.db_select as model


class Select(ttk.Frame):

    def __init__(
            self,
            app,
            frame,
    ):
        super().__init__(frame)
        self.app = app
        # temp variables
        self.selected_ledger = tk.StringVar(self.app)

        # widget definitions
        self.title_label = ttk.Label(
            self,
            text="We_Square?",
            font=tkf.Font(
                size=30,
                family="Impact"
            )
        )
        self.tooltip_checkbox = ttk.Checkbutton(
            self,
            text="Enable Tooltips"
        )
        self.select_label = ttk.Label(
            self,
            text="Select Existing"
        )
        self.select_dropdown = ttk.OptionMenu(
            self,
            variable=self.selected_ledger,
        )
        self.create_button = ttk.Button(
            self,
            text="New Ledger",
            command=self.raise_create_frame
        )
        self.ledger_button = ttk.Button(
            self,
            text="View Selected",
            command=self.raise_ledger_frame
        )

        # configure grid rows
        self.grid_rowconfigure(0, weight=5)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=1)
        # configure grid columns
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # frame layout
        self.title_label.grid(
            column=0,
            row=0,
            columnspan=2
        )
        self.tooltip_checkbox.grid(
            column=0,
            row=1,
            columnspan=1,
            sticky="W"
        )
        self.select_label.grid(
            column=1,
            row=1,
            columnspan=1,
            sticky="w"
        )
        self.select_dropdown.grid(
            column=1,
            row=2,
            columnspan=1,
            sticky="WE"
        )
        self.create_button.grid(
            column=0,
            row=3,
            columnspan=1,
            sticky="WE"
        )
        self.ledger_button.grid(
            column=1,
            row=3,
            columnspan=1,
            sticky="WE"
        )

    def update(self):
        ledger_list = model.retrieve_ledger_titles(self.app)
        if len(ledger_list) == 0:
            self.selected_ledger.set('')
            self.select_dropdown['menu'].delete(0, tk.END)
            self.ledger_button['state'] = tk.DISABLED
        else:
            self.select_dropdown['menu'].delete(0, tk.END)
            for ledger in ledger_list:
                self.select_dropdown['menu'].add_command(
                    label=ledger,
                    command=tk._setit(self.selected_ledger, ledger)
                )
            self.selected_ledger.set(ledger_list[0])
            self.ledger_button['state'] = tk.NORMAL

    def raise_create_frame(self):
        self.app.raise_frame("create")

    def raise_ledger_frame(self):
        title = self.selected_ledger.get()
        index = model.retrieve_ledger_index_by_title(self.app, title)
        self.app.raise_frame("ledger", index)
