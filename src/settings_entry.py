import tkinter as tk

from constants import *

class EntrySettings(tk.Frame):
    def __init__(self, master):
        self.master = master

        tk.Frame.__init__(
            self,
            master,
            width=WIDTH - PADDING_BIG * 2, 
            height=120
        )

        self.labels = []
        self.buttons = []

        self.create_widgets()
        self.refresh_colors()

    def create_widgets(self):

        self.title_label = tk.Label(
            self,
            text="Entry",
            justify=tk.CENTER
        )
        self.title_label.grid(
            row=0,
            column=0,
            columnspan=10
        )
        self.labels.append(self.title_label)

        self.show_checkboxes_var = tk.IntVar()
        self.show_checkboxes = tk.Checkbutton(
            self,
            text="Show checkboxes",
            variable=self.show_checkboxes_var,
            command=self.show_checkboxes_pressed
        )
        self.show_checkboxes.grid(
            row=1, 
            column=0,
            padx=PADDING,
            pady=PADDING
        )
        self.buttons.append(self.show_checkboxes)

    def refresh_colors(self):
        self.colors = self.master.master.colors_obj.get_colors()

        self.configure(
            bg=self.colors["BG2"]
        )

        for label in self.labels:
            label.configure(
                bg=self.colors["BG2"],
                fg=self.colors["HL2"]
            )

        for button in self.buttons:
            button.configure(
                highlightbackground=self.colors["BG2"],
                bg=self.colors["BG2"],
                fg=self.colors["HL2"]
            )

    def show_checkboxes_pressed(self):
        if (self.show_checkboxes_var.get() == 1):
            self.master.master.top_frame.show_checkboxes = True
            self.master.master.top_frame.refresh_entries()
        else:
            self.master.master.top_frame.show_checkboxes = False
            self.master.master.top_frame.refresh_entries()