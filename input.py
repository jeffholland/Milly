import tkinter as tk

from constants import *
from data import *

class Input(tk.Frame):
    def __init__(self, width, height, bg, master=None):
        tk.Frame.__init__(
            self, 
            master, 
            width=width, 
            height=height, 
            bg=bg)
        self.create_widgets()

    def submit(self):
        add_entry(self.input.get("1.0", "end"))
        self.master.refresh_entries()
        self.input.delete("1.0", "end")

    def create_widgets(self):
        self.input = tk.Text(
            self, 
            height=10, 
            bg="grey")
        self.input.grid(row=0, column=0, padx=PADDING, pady=PADDING, rowspan=10)

        self.submit_button = tk.Button(self, text="Submit", command=self.submit)
        self.submit_button.grid(row=0, column=1, padx=PADDING, pady=PADDING)

        self.save_button = tk.Button(self, text="Save", command=save)
        self.save_button.grid(row=1, column=1, padx=PADDING, pady=PADDING)