import tkinter as tk
import tkinter.font as f


class Home(tk.Frame):

    def __init__(self, container):
        super().__init__()

        self.container = container

        # font definitions
        button_font = f.Font(
            size=14
        )
        header_font = f.Font(
            size=20,
            family="Impact"
        )

        # widget definitions
        header_label = tk.Label(
            master=self,
            text="WE_SQUARE?",
            font=header_font
        )

        create_button = tk.Button(
            master=self,
            text="Create Ledger",
            font=button_font
        )

        select_button = tk.Button(
            master=self,
            text="Select Ledger",
            font=button_font
        )

        # window layout
        header_label.grid(
            column=0,
            row=0,
            columnspan=2,
            pady=(20, 0)
        )
        create_button.grid(
            column=0,
            row=1,
            columnspan=1,
            padx=(20, 5),
            pady=(20, 20)
        )
        select_button.grid(
            column=1,
            row=1,
            columnspan=1,
            padx=(5, 20),
            pady=(20, 20)
        )


if __name__ == "__main__":
    app = tk.Tk()
    app.title("We_Square?")
    view = Home(app)
    view.pack()
    app.mainloop()
