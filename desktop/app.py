# import packages
import os
import pickle
import tkinter as tk
import tkinter.ttk as ttk

# import app views
from desktop.views.create import Create
from desktop.views.ledger import Ledger
from desktop.views.select import Select


class App(tk.Tk):

    def __init__(self):
        super().__init__()
        # configurations
        self.title("We_Square?")
        self.iconbitmap("resources/icon.ico")
        self.resizable(False, False)
        # primary data
        self.ledgers = []

        # override window delete protocol to save data
        self.protocol("WM_DELETE_WINDOW", self.write_data)

        # top level frame
        container = ttk.Frame(
            self,
            padding='10',
        )
        container.pack()

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
        self.read_data()

        self.raise_frame("select")

    def read_data(self):
        path = '.\\data\\objects'
        file_list = os.listdir(path)
        for file in file_list:
            file_path = path + "\\" + file
            with open(file_path, "rb") as ledger:
                self.ledgers.append(pickle.load(ledger))

    def write_data(self):
        # remove previous files
        path = '.\\data\\objects'
        file_list = os.listdir(path)
        for file in file_list:
            file_path = path + "\\" + file
            os.remove(file_path)
        # write new files
        for index, ledger in enumerate(self.ledgers):
            file_name = ".\\data\\objects\\ledger_" + str(index)
            with open(file_name, "wb") as file:
                pickle.dump(ledger, file)
        # close window
        self.destroy()

    def raise_frame(self, frame, ledger_index=None):
        # update available ledgers
        if frame == "select":
            self.frames["select"].update()

        # set data for ledger frame
        if ledger_index is not None:
            self.frames["ledger"].ledger = self.ledgers[ledger_index]
            self.frames["ledger"].reset_fields(True, True, True, True, True)
            self.frames["ledger"].update(True, True, True, True)

        # raise frame
        self.frames[frame].tkraise()


if __name__ == "__main__":
    app = App()
    app.mainloop()
