# import packages
import tkinter as tk
import tkinter.font as font

# import app views
from views.home import Home
from views.create import Create
from views.select import Select
from views.ledger import Ledger
from views.total import Total

# import app model
# from model.db_create import
# from model.db_select import
# from model.db_ledger import


class App(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title("We_Square?")
        self.resizable(False, False)

        # top level frame
        container = tk.Frame(
            self,
            padx=20,
            pady=20
        )
        container.pack()
        # container.pack(side="top", fill="both", expand=True)
        # container.grid_rowconfigure(0, weight=1)
        # container.grid_columnconfigure(0, weight=1)

        # style definitions
        title_font = font.Font(
            size=30,
            family="Impact"
        )
        nav_font = font.Font(
            size=12
        ),

        # views
        self.frames = {
            "home": Home(self, container, title_font, nav_font),
            "create": Create(self, container, nav_font),
            "select": Select(self, container, nav_font),
            "ledger": Ledger(self, container, nav_font),
            "total": Total(self, container, nav_font)
        }

        for frame in self.frames:
            self.frames[frame].grid(
                row=0,
                column=0,
                sticky="nsew"
            )

        self.raise_frame("home")

    def raise_frame(self, frame):
        self.frames[frame].tkraise()


if __name__ == "__main__":
    app = App()
    app.mainloop()
