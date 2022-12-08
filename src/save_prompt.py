import tkinter as tk

from constants import *

class SavePrompt(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        self.window = tk.Toplevel(master)
        self.window.title("Save prompt")
        self.window.geometry("370x100")

        self.create_widgets()

    def create_widgets(self):
        self.label = tk.Label(
            self.window,
            text="Would you like to save changes?",
            fg=colors["HL1"]
        )
        self.label.grid(
            row=0,
            column=0,
            columnspan=4,
            padx=PADDING,
            pady=PADDING
        )

        self.yes_button = tk.Button(
            self.window,
            text="Yes"
        )
        self.yes_button.grid(
            row=1,
            column=0,
            padx=PADDING,
            pady=PADDING
        )

        self.no_button = tk.Button(
            self.window,
            text="No"
        )
        self.no_button.grid(
            row=1,
            column=1,
            padx=PADDING,
            pady=PADDING
        )

        self.cancel_button = tk.Button(
            self.window,
            text="Cancel"
        )
        self.cancel_button.grid(
            row=1,
            column=2,
            padx=PADDING,
            pady=PADDING
        )

        self.save_new_button = tk.Button(
            self.window,
            text="Save new"
        )
        self.save_new_button.grid(
            row=1,
            column=3,
            padx=PADDING,
            pady=PADDING
        )