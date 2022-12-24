import tkinter as tk

from constants import *

class Template(tk.Frame):
    def __init__(self, master):

        tk.Frame.__init__(
            self,
            master,
            width=WIDTH - PADDING_BIG * 2, 
            height=120
        )
        self.master = master

        self.labels = []
        self.buttons = []

        self.create_widgets()



    def create_widgets(self):

        self.title_label = tk.Label(
            self,
            text="Template",
            justify=tk.CENTER
        )
        self.title_label.grid(
            row=0,
            column=0,
            columnspan=10
        )
        self.labels.append(self.title_label)



    def refresh_colors(self, colors):
        self.colors = colors

        for label in self.labels:
            label.configure(
                bg=self.colors["BG1"],
                fg=self.colors["HL2"]
            )

        for button in self.buttons:
            button.configure(
                highlightbackground=self.colors["BG1"]
            )
            if PLATFORM == "Windows":
                button.configure(
                    bg=self.colors["BG2"],
                    fg=self.colors["HL2"]
                )