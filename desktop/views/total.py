import tkinter as tk


class Total(tk.Frame):

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
            text="WE_SQUARE?",
        )
        summary_label = tk.Label(
            master=self,
            text="[LEDGER SUMMARY]"
        )
        view_ledger_button = tk.Button(
            master=self,
            text="Back to Ledger",
            font=nav_font,
            command=self.raise_ledger_frame
        )
        send_ledger_button = tk.Button(
            master=self,
            text="Send Ledger",
            font=nav_font,
            command=self.raise_home_frame,
        )

        # frame layout
        header_label.grid(
            column=0,
            row=0,
            columnspan=2
        )
        summary_label.grid(
            column=0,
            row=1,
            columnspan=2
        )
        view_ledger_button.grid(
            column=0,
            row=2,
            columnspan=1,
            sticky="EW",
        )
        send_ledger_button.grid(
            column=1,
            row=2,
            columnspan=1,
            sticky="EW",
        )

    def raise_ledger_frame(self):
        self.app.raise_frame("ledger")

    def raise_home_frame(self):
        self.app.raise_frame("home")
