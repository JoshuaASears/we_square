import tkinter as tk


class Home(tk.Frame):

    def __init__(
            self,
            app,
            frame,
            title_font,
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
            text="WE_SQUARE?",
            font=title_font
        )

        create_button = tk.Button(
            master=self,
            text="Create Ledger",
            font=nav_font,
            command=self.raise_create_frame
        )

        select_button = tk.Button(
            master=self,
            text="Select Ledger",
            font=nav_font,
            command=self.raise_select_frame,
        )

        # frame layout
        header_label.grid(
            column=0,
            row=0,
            columnspan=2
        )
        create_button.grid(
            column=0,
            row=1,
            columnspan=1,
            sticky="EW",
        )
        select_button.grid(
            column=1,
            row=1,
            columnspan=1,
            sticky="EW",
        )

    def raise_create_frame(self):
        self.app.raise_frame("create")

    def raise_select_frame(self):
        self.app.raise_frame("select")
