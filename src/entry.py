import tkinter as tk
import tkinter.font as tkFont

from constants import *
from data import remove_entry

class Entry(tk.Frame):
    def __init__(self, date, time, text, width, height, bg, index, master=None):

        # TODO: make height dynamic according to length of text
        tk.Frame.__init__(
            self, 
            master, 
            width=width, 
            height=height, 
            bg=bg)

        self.date = date
        self.time = time
        self.text = text
        self.bg = bg
        self.index = index

        # Truncated width
        if width < 200:
            self.width = 200
        else:
            self.width = width

        self.font = tkFont.Font(
            family=ENTRY_FONT_FAMILY, 
            size=ENTRY_FONT_SIZE)
        self.font_bold = tkFont.Font(
            family=ENTRY_FONT_FAMILY, 
            size=ENTRY_FONT_SIZE, 
            weight="bold")

        self.create_widgets()

    def x_pressed(self):
        remove_entry(self.index)
        self.master.master.master.refresh_entries()

    def create_widgets(self):
        self.date_label = tk.Label(
            self, 
            text=self.date,
            font=self.font_bold)
        self.date_label.grid(
            row=0, 
            column=0, 
            sticky=tk.W)

        self.time_label = tk.Label(
            self, 
            text=self.time,
            font=self.font)
        self.time_label.grid(
            row=0, 
            column=2,
            sticky=tk.E)

        if len(self.text) < 25:

            self.text_label = tk.Label(
                self, 
                text=self.text,
                bg=self.bg, 
                fg=colors["HL2"], 
                font=self.font,
                wraplength=720,
                width=20)
            self.text_label.grid(
                row=1, 
                column=0, 
                padx=PADDING,
                pady=PADDING,
                columnspan=4)

        else:

            self.text_label = tk.Label(
                self, 
                text=self.text,
                bg=self.bg, 
                fg=colors["HL2"], 
                font=self.font,
                wraplength=720)
            self.text_label.grid(
                row=1, 
                column=0, 
                padx=PADDING,
                pady=PADDING,
                columnspan=4)


        # Grid_bbox gives dimensions of Entry
        self.update()
        # print(self.grid_bbox(column=0, row=1))

        self.xbutton = tk.Button(
            self,
            text="x",
            highlightbackground=colors["BG2"],
            width=1,
            command=self.x_pressed
        )
        self.xbutton.grid(
            row=0,
            column=3,
            sticky=tk.NE
        )