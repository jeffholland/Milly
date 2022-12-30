import tkinter as tk
import tkinter.font as tkFont

from constants import *
from entry import Entry

class Group(tk.Frame):
    def __init__(self, master, width, entry_height, entries_data, name):
        self.entry_height = entry_height

        tk.Frame.__init__(
            self, 
            master,
            width=width,
            height=entry_height
        )

        self.width = width
        self.height = entry_height
        self.name = name
        self.master = master
        self.entries_data = entries_data

        self.show_dates = True
        self.show_times = True

        self.entries = []

        self.create_widgets()



    def create_widgets(self):

        # Name label

        self.name_label = tk.Label(
            self,
            text=self.name
        )
        self.name_label.grid(
            row=0,
            column=0,
            columnspan=5,
            padx=PADDING,
            pady=PADDING
        )

        # Show entries

        for count in range(len(self.entries_data)):
            try:
                checked_bool = self.entries_data[count]["checked"]
            except KeyError:
                checked_bool = False

            entry_date = None
            if self.show_dates:
                entry_date = self.entries_data[count]["date"]
            entry_time = None
            if self.show_times:
                entry_time = self.entries_data[count]["time"]

            self.entries.append(Entry(
                self,
                date=entry_date,
                time=entry_time,
                menu=True,
                text=self.entries_data[count]["text"],
                width=self.width - PADDING * 4,
                height=self.entry_height,
                index=count,
                font=tkFont.Font(self, family="Helvetica", size="12"),
                checkbox=True,
                checked=checked_bool,
                group=self.name
            ))
            self.entries[count].grid_propagate(0)
            self.entries[count].grid(
                row=count + 1, 
                column=0,
                padx=PADDING, 
                pady=PADDING
            )
        self.calculate_height()

    def refresh_colors(self, colors):
        self.colors = colors

        self.configure(bg=self.colors["BG2"])

        self.name_label.configure(
            bg=self.colors["BG2"],
            fg=self.colors["HL2"]
        )

    def calculate_height(self):
        self.height = 0

        for entry in self.entries:
            self.height += entry.height + PADDING * 2

        self.height += 80

        self.configure(height=self.height)

    def delete(self):
        for entry in self.entries:
            entry.group = None
            entry.master = self.master