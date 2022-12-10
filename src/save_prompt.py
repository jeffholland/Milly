import tkinter as tk

from sys import exit

from colors import get_colors
from constants import *

class SavePrompt(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(
            self, 
            master
        )

        self.window = tk.Toplevel(
            master
        )
        self.window.title("Save prompt")
        self.window.geometry("250x100")
        # self.window.geometry("370x100")

        self.create_widgets()

        self.refresh_colors()

    def yes_pressed(self):
        self.master.save(and_exit=True)

    def no_pressed(self):
        exit()

    def cancel_pressed(self):
        self.window.destroy()

    # def save_new_pressed(self):
    #     print("save new")

    def create_widgets(self):
        self.label = tk.Label(
            self.window,
            text="Would you like to save changes?"
        )
        self.label.grid(
            row=0,
            column=0,
            columnspan=3,
            padx=PADDING,
            pady=PADDING
        )

        self.yes_button = tk.Button(
            self.window,
            text="Yes",
            command=self.yes_pressed
        )
        self.yes_button.grid(
            row=1,
            column=0,
            padx=PADDING,
            pady=PADDING
        )
        self.yes_button.focus_set()

        self.no_button = tk.Button(
            self.window,
            text="No",
            command=self.no_pressed
        )
        self.no_button.grid(
            row=1,
            column=1,
            padx=PADDING,
            pady=PADDING
        )

        self.cancel_button = tk.Button(
            self.window,
            text="Cancel",
            command=self.cancel_pressed
        )
        self.cancel_button.grid(
            row=1,
            column=2,
            padx=PADDING,
            pady=PADDING
        )

        # self.save_new_button = tk.Button(
        #     self.window,
        #     text="Save new",
        #     command=self.save_new_pressed
        # )
        # self.save_new_button.grid(
        #     row=1,
        #     column=3,
        #     padx=PADDING,
        #     pady=PADDING
        # )

    def refresh_colors(self):
        self.colors = get_colors()

        self.window.configure(
            bg=self.colors["BG2"]
        )

        self.label.configure(
            bg=self.colors["BG2"]
        )
        
        self.yes_button.configure(
            highlightbackground=self.colors["BG2"],
            highlightcolor=self.colors["BG1"]
        )

        self.no_button.configure(
            highlightbackground=self.colors["BG2"],
            highlightcolor=self.colors["BG1"]
        )

        self.cancel_button.configure(
            highlightbackground=self.colors["BG2"],
            highlightcolor=self.colors["BG1"]
        )