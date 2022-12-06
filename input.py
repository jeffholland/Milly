import tkinter as tk
import tkinter.font as tkFont

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

        self.inputFont = tkFont.Font(
            self, 
            family="Courier New", 
            size=INPUT_FONT_SIZE)

        self.num_buttons = 4

        self.create_widgets()

    def submit(self):
        add_entry(self.input.get("1.0", "end"))
        self.master.refresh_entries()
        self.input.delete("1.0", "end")

    def save(self):
        save("data.json")

    def load(self):
        load("data.json")
        self.master.refresh_entries()

    def clear(self):
        clear()
        self.master.refresh_entries()

    def create_widgets(self):
        self.input = tk.Text(
            self, 
            height=INPUT_HEIGHT, 
            width=INPUT_WIDTH,
            bg="lightgrey",
            fg="black",
            font=self.inputFont)
        self.input.grid(
            row=0, 
            column=0, 
            padx=PADDING, 
            pady=PADDING,
            rowspan=self.num_buttons)

        self.submit_button = tk.Button(
            self, 
            text="Submit", 
            command=self.submit,
            highlightbackground="black")
        self.submit_button.grid(
            row=0, 
            column=1, 
            padx=PADDING)

        self.save_button = tk.Button(
            self, 
            text="Save", 
            command=self.save,
            highlightbackground="black")
        self.save_button.grid(
            row=1, 
            column=1, 
            padx=PADDING)

        self.load_button = tk.Button(
            self,
            text="Load",
            command=self.load,
            highlightbackground="black")
        self.load_button.grid(
            row=2, 
            column=1, 
            padx=PADDING)

        self.clear_button = tk.Button(
            self,
            text="Clear",
            command=self.clear,
            highlightbackground="black")
        self.clear_button.grid(
            row=3,
            column=1,
            padx=PADDING)