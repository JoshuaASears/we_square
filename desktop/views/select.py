import tkinter.ttk as ttk
import tkinter.font as tkf


class Select(ttk.Frame):

    def __init__(
            self,
            app,
            frame,
    ):
        super().__init__(frame)
        self.app = app
        # widget definitions
        title_label = ttk.Label(
            self,
            text="We_Square?",
            font=tkf.Font(
                size=30,
                family="Impact"
            )
        )
        tooltip_checkbox = ttk.Checkbutton(
            self,
            text="Enable Tooltips"
        )
        select_label = ttk.Label(
            self,
            text="Select Existing"
        )
        select_dropdown = ttk.OptionMenu(
            self,
            variable=None,
        )
        create_button = ttk.Button(
            self,
            text="New Ledger",
            command=self.raise_create_frame
        )
        ledger_button = ttk.Button(
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
        title_label.grid(
            column=0,
            row=0,
            columnspan=2
        )
        tooltip_checkbox.grid(
            column=0,
            row=1,
            columnspan=1,
            sticky="W"
        )
        select_label.grid(
            column=1,
            row=1,
            columnspan=1,
            sticky="w"
        )
        select_dropdown.grid(
            column=1,
            row=2,
            columnspan=1,
            sticky="WE"
        )
        create_button.grid(
            column=0,
            row=3,
            columnspan=1,
            sticky="WE"
        )
        ledger_button.grid(
            column=1,
            row=3,
            columnspan=1,
            sticky="WE"
        )

    def raise_create_frame(self):
        self.app.raise_frame("create")

    def raise_ledger_frame(self):
        self.app.raise_frame("ledger")
