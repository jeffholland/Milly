import tkinter as tk

from sys import exit

from constants import *

class SavePrompt(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(
            self, 
            master,
            bg=colors["BG2"]
        )

        self.window = tk.Toplevel(
            master,
            bg=colors["BG2"]
        )
        self.window.title("Save prompt")
        self.window.geometry("250x100")
        # self.window.geometry("370x100")

        self.create_widgets()

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
            text="Would you like to save changes?",
            bg=colors["BG2"],
            fg=colors["HL2"]
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
            command=self.yes_pressed,
            highlightbackground=colors["BG2"],
            highlightcolor=colors["BG1"],
            fg=colors["HL2"]
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
            command=self.no_pressed,
            highlightbackground=colors["BG2"],
            highlightcolor=colors["BG1"],
            fg=colors["HL2"]
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
            command=self.cancel_pressed,
            highlightbackground=colors["BG2"],
            highlightcolor=colors["BG1"],
            fg=colors["HL2"]
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