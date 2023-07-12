import tkinter as tk
import tkinter.ttk as ttk


class Select(tk.Frame):

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
            text="Select Ledger"
        )
        select_label = tk.Label(
            master=self,
            text="Select Existing"
        )
        select_dropdown = ttk.Combobox(
            master=self,
        )
        home_button = tk.Button(
            master=self,
            text="Home",
            font=nav_font,
            command=self.raise_home_frame
        )
        ledger_button = tk.Button(
            master=self,
            text="View Ledger",
            font=nav_font,
            command=self.raise_ledger_frame
        )

        # frame layout
        header_label.grid(
            column=0,
            row=0,
        )
        select_label.grid(
            column=0,
            row=1,
            columnspan=1
        )
        select_dropdown.grid(
            column=0,
            row=2,
            columnspan=1
        )
        home_button.grid(
            column=0,
            row=3,
            columnspan=1,
            sticky="EW",
        )
        ledger_button.grid(
            column=1,
            row=3,
            columnspan=1,
            sticky="EW",
        )

    def raise_home_frame(self):
        self.app.raise_frame("home")

    def raise_ledger_frame(self):
        self.app.raise_frame("ledger")
