import tkinter as tk

from constants import colors, HEIGHT, WIDTH
from entries import Entries
from input import Input

class Application(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.grid(row=0, column=0)
        self.create_widgets()

    def create_widgets(self):
        self.top_frame_height = (HEIGHT // 3) * 2

        print(colors)

        self.top_frame = Entries(
            width=WIDTH, 
            height=self.top_frame_height,
            bg=colors["HL1"],
            master=self)
        self.top_frame.grid_propagate(0)
        self.top_frame.grid(row=0, column=0)

        self.bottom_frame_height = HEIGHT // 3

        self.bottom_frame = Input(
            width=WIDTH,
            height=self.bottom_frame_height,
            bg=colors["BG2"],
            master=self
        )
        self.bottom_frame.grid_propagate(0)
        self.bottom_frame.grid(row=1, column=0)

    def refresh_entries(self):
        self.top_frame.refresh_entries()
        


app = Application()
app.master.title("Diary")
app.master.geometry(str(WIDTH) + "x" + str(HEIGHT))
app.mainloop()