import sys
import tkinter as tk
import tkinter.font as f

# views
sys.path.append("../views")
import home



class App(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title("We_Square?")

        # style definitions
        h_font = f.Font(
            size=20,
            family="Impact"
        )
        p = 20
        view = Home(app, h_font, p)
        view.pack()


if __name__ == "__main__":
    app = App()
    app.mainloop()