import tkinter as tk

import hashlib

from constants import *
from data import remove_group
from entry import Entry
from group_menu import GroupMenu

class Group(tk.Frame):
    def __init__(self, master, width, entry_height, 
        entries_data, name, font, show_dates, show_times):
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
        self.font = font

        # Sort entries data by checked
        self.entries_data = entries_data
        self.sort_by_checked()

        self.show_dates = show_dates
        self.show_times = show_times

        self.entries = []

        self.create_widgets()


    # IMPORTANT: This is the function in which the entries get shown
    # on the screen.

    def show_entries(self):

        count = 0

        for entry in self.entries_data:

            # Show checkboxes

            try:
                checked_bool = self.entries_data[count]["checked"]
            except KeyError:
                checked_bool = False

            # Show dates and times

            entry_date = None
            if self.show_dates:
                entry_date = self.entries_data[count]["date"]
            entry_time = None
            if self.show_times:
                entry_time = self.entries_data[count]["time"]

            # Show entries

            text = entry["text"]

            self.entries.append(Entry(
                self,
                date=entry_date,
                time=entry_time,
                menu=True,
                text=text,
                width=self.width - PADDING * 4,
                height=self.entry_height,
                index=count,
                font=self.font,
                checkbox=True,
                checked=checked_bool,
                group=self.name
            ))
            self.entries[count].grid_propagate(0)
            self.entries[count].grid(
                row=count + 1, 
                column=0,
                padx=PADDING, 
                pady=PADDING,
                columnspan=2
            )

            count += 1


    def create_widgets(self):

        # Group menu - contains name label and buttons

        self.group_menu = GroupMenu(
            self,
            self.name,
            self.font
        )
        self.group_menu.grid(
            row=0,
            column=0
        )

        # Show entries

        self.show_entries()

        self.calculate_height()



    def refresh_colors(self, colors):
        self.colors = colors

        self.configure(bg=self.colors["BG2"])

        for entry in self.entries:
            entry.refresh_colors(colors)

        self.group_menu.refresh_colors(colors)



    def calculate_height(self):
        self.height = 0

        for entry in self.entries:
            self.height += entry.height + PADDING * 2

        self.height += 80

        self.configure(height=self.height)

    def delete(self):
        remove_group(self.name)
        self.master.master.master.refresh_entries()

    def sort_by_checked(self):

        switch = False
        count = 0

        for entry in list(self.entries_data):

            try:
                checked = entry["checked"]
            except KeyError:
                entry["checked"] = False
                checked = entry["checked"]

            if switch:
                if not checked:
                    self.entries_data.pop(count)
                    self.entries_data.insert(0, entry)
            if checked:
                switch = True

            count += 1

    def get_num_entries(self):
        return len(self.entries_data)

    def set_name(self, new_name):
        self.name = new_name
        self.master.master.master.refresh_group_names()