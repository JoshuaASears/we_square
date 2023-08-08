
import tkinter as tk
import tkinter.font as tkf
import tkinter.ttk as ttk


class Select(ttk.Frame):

    def __init__(self, frame, callbacks):
        super().__init__(frame)
        # temp variables
        self._selected_ledger = tk.StringVar(self)

        # widget definitions
        self._title_label = ttk.Label(
            self,
            text="We_Square?",
            font=tkf.Font(
                size=30,
                family="Impact"
            )
        )
        self._tooltip_checkbox = ttk.Checkbutton(
            self,
            text="Enable Tooltips"
        )
        self._select_label = ttk.Label(
            self,
            text="Select Existing"
        )
        self._select_dropdown = ttk.OptionMenu(
            self,
            variable=self._selected_ledger,
        )
        self._create_button = ttk.Button(
            self,
            text="New Ledger",
            command=callbacks[0]
        )
        self._ledger_button = ttk.Button(
            self,
            text="View Selected",
            command=callbacks[1]
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
        self._title_label.grid(
            column=0,
            row=0,
            columnspan=2
        )
        self._tooltip_checkbox.grid(
            column=0,
            row=1,
            columnspan=1,
            sticky="W"
        )
        self._select_label.grid(
            column=1,
            row=1,
            columnspan=1,
            sticky="w"
        )
        self._select_dropdown.grid(
            column=1,
            row=2,
            columnspan=1,
            sticky="WE"
        )
        self._create_button.grid(
            column=0,
            row=3,
            columnspan=1,
            sticky="WE"
        )
        self._ledger_button.grid(
            column=1,
            row=3,
            columnspan=1,
            sticky="WE"
        )

    def get_selected_ledger(self):
        return self._selected_ledger.get()

    def set_ledger_list(self, ledger_list):
        self._select_dropdown['menu'].delete(0, tk.END)
        for ledger in ledger_list:
            self._select_dropdown['menu'].add_command(
                label=ledger,
                command=tk._setit(self._selected_ledger, ledger)
            )
        self._selected_ledger.set(ledger_list[0])
        self._ledger_button['state'] = tk.NORMAL

    def disable_ledger_select(self):
        self._selected_ledger.set('')
        self._select_dropdown['menu'].delete(0, tk.END)
        self._ledger_button['state'] = tk.DISABLED
