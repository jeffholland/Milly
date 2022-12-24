import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont

from constants import *

class FontSettings(tk.Frame):
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
            text="Font",
            justify=tk.CENTER
        )
        self.title_label.grid(
            row=0,
            column=0,
            columnspan=10
        )
        self.labels.append(self.title_label)

        self.font_selector = ttk.Combobox(
            self
        )
        self.font_selector.grid(
            row=1, 
            column=0,
            padx=PADDING,
            pady=PADDING
        )
        self.font_selector["values"] = tkFont.families()



    def refresh_colors(self, colors):
        self.colors = colors

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
                highlightbackground=self.colors["BG1"]
            )
            if PLATFORM == "Windows":
                button.configure(
                    bg=self.colors["BG2"],
                    fg=self.colors["HL2"]
                )