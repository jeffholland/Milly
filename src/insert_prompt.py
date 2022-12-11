import tkinter as tk

from data import get_entries

class InsertPrompt(tk.Frame):
    def __init__(self, master):
        self.master = master
        self.window = tk.Toplevel(master)

        self.max_val = len(get_entries())

        self.create_widgets()

    def create_widgets(self):
        self.spinbox = tk.Spinbox(
            self.window,
            from_=0,
            to_=len(get_entries())
        )
        self.spinbox.grid(row=0, column=0)