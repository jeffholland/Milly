import tkinter as tk
import tkinter.font as tkFont

from colors import get_colors
from constants import *
from data import *

class Entry(tk.Frame):
    def __init__(self, date, time, text, width, height, index, master=None):

        # TODO: make height dynamic according to length of text
        tk.Frame.__init__(
            self, 
            master, 
            width=width,
            height=height
        )

        # Variables

        self.date = date
        self.time = time
        self.text = text
        self.index = index

        # Height varies based on length of text

        if len(text) > 100:
            new_height = height + ((len(text) - 100) // 6)
            self.configure(height=new_height)

        # Font

        self.font = tkFont.Font(
            family=ENTRY_FONT_FAMILY, 
            size=ENTRY_FONT_SIZE
        )
        self.font_bold = tkFont.Font(
            family=ENTRY_FONT_FAMILY, 
            size=ENTRY_FONT_SIZE, 
            weight="bold"
        )

        self.create_widgets()

        self.refresh_colors()


    def create_widgets(self):
        self.date_label = tk.Label(
            self, 
            text=self.date,
            font=self.font_bold
        )
        self.date_label.grid(
            row=0, 
            column=0, 
            sticky=tk.W
        )

        self.time_label = tk.Label(
            self, 
            text=self.time,
            font=self.font
        )
        self.time_label.grid(
            row=0, 
            column=2
        )

        self.text_label = tk.Label(
            self, 
            text=self.text,
            font=self.font,
            wraplength=720,
            anchor=tk.NW,
            justify=tk.LEFT
        )

        if len(self.text) < 40:
            self.text_label.configure(
                width=ENTRY_MIN_WIDTH
            )

        self.text_label.grid(
            row=1, 
            column=0, 
            padx=PADDING,
            pady=PADDING,
            columnspan=6
        )

        self.update()

        # BUTTONS

        self.upbutton = tk.Button(
            self,
            text="up",
            width=1,
            command=self.up_pressed
        )
        self.upbutton.grid(
            row=0,
            column=3
        )

        self.downbutton = tk.Button(
            self,
            text="down",
            width=1,
            command=self.down_pressed
        )

        self.downbutton.grid(
            row=0,
            column=4
        )

        self.xbutton = tk.Button(
            self,
            text="x",
            width=1,
            command=self.x_pressed
        )
        self.xbutton.grid(
            row=0,
            column=5,
            sticky=tk.E
        )

    def refresh_colors(self):
        self.colors = get_colors()

        self.configure(
            bg=self.colors["BG1"]
        )

        self.date_label.configure(
            bg=self.colors["BG1"], 
            fg=self.colors["HL2"]
        )

        self.time_label.configure(
            bg=self.colors["BG1"], 
            fg=self.colors["HL2"]
        )

        self.text_label.configure(
            bg=self.colors["BG1"], 
            fg=self.colors["HL2"]
        )

        self.upbutton.configure(
            highlightbackground=self.colors["BG1"]
        )
        self.downbutton.configure(
            highlightbackground=self.colors["BG1"]
        )
        self.xbutton.configure(
            highlightbackground=self.colors["BG1"]
        )

    # Handlers

    def x_pressed(self):
        remove_entry(self.index)
        self.master.master.master.refresh_entries()

    def up_pressed(self):
        if self.index > 0:
            swap_entry(self.index - 1, self.index)
            self.master.master.master.refresh_entries()

    def down_pressed(self):
        if self.index < len(get_entries()) - 1:
            swap_entry(self.index, self.index + 1)
            self.master.master.master.refresh_entries()