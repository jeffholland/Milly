import tkinter as tk

from constants import *

class SavePrompt(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        self.window = tk.Toplevel(master)
        self.window.title("Save prompt")
        self.window.geometry("200x200")

    def create_widgets(self):
        self.label = tk.Label(
            self,
            text="Would you like to save changes?"
        )
        self.label.grid(
            row=0,
            column=0,
            columnspan=4
        )

        self.yes_button = tk.Button(
            self,
            text="Yes"
        )
        self.yes_button.grid(
            row=1,
            column=0
        )

        self.no_button = tk.Button(
            self,
            text="No"
        )
        self.no_button.grid(
            row=1,
            column=3
        )

        self.cancel_button = tk.Button(
            self,
            text="Cancel"
        )
        self.cancel_button.grid(
            row=1,
            column=2
        )

        self.save_new_button = tk.Button(
            self,
            text="Save new"
        )
        self.save_new_button.grid(
            row=1,
            column=1
        )