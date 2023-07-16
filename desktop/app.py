# import packages
import tkinter as tk
import tkinter.ttk as ttk

# import app views
from views.create import Create
from views.select import Select
from views.ledger import Ledger

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

    def raise_frame(self, frame):
        self.frames[frame].tkraise()


if __name__ == "__main__":
    app = App()
    app.mainloop()
