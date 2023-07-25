# import packages
import tkinter as tk
import tkinter.ttk as ttk

# import app views
from desktop.views.create import Create
from desktop.views.select import Select
from desktop.views.ledger import Ledger

# import app model
# from model.db_create import
# from model.db_select import
# from model.db_ledger import


class App(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title("We_Square?")
        self.iconbitmap("resources/icon.ico")
        self.resizable(False, False)
        self.ledgers = []

        # top level frame
        container = ttk.Frame(
            self,
            padding='10',
        )
        container.pack()
        # container.pack(side="top", fill="both", expand=True)
        # container.grid_rowconfigure(0, weight=1)
        # container.grid_columnconfigure(0, weight=1)

        # views
        self.frames = {
            "select": Select(self, container,),
            "create": Create(self, container,),
            "ledger": Ledger(self, container,),
        }

        for frame in self.frames:
            self.frames[frame].grid(
                row=0,
                column=0,
                sticky="nsew"
            )

        self.raise_frame("select")

    def raise_frame(self, frame, ledger_index=None):
        # update available ledgers
        if frame != "create":
            self.frames["select"].update()

        # set data for ledger frame
        if ledger_index is not None:
            self.frames["ledger"].ledger = self.ledgers[ledger_index]
            self.frames["ledger"].update(True, True, True, True)

        # raise frame
        self.frames[frame].tkraise()


if __name__ == "__main__":
    app = App()
    app.mainloop()
