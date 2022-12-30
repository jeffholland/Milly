import tkinter as tk
import tkinter.font as tkFont

from constants import *
from entry import Entry

class Group(tk.Frame):
    def __init__(self, master, width, entry_height, entries_data, name, font):
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
        self.font = font

        self.show_dates = True
        self.show_times = True

        self.entries = []

        self.title_font = tkFont.Font(self, family="Helvetica", size=20)

        self.create_widgets()



    def create_widgets(self):

        # Name label

        self.name_label = tk.Label(
            self,
            text=self.name,
            font=self.title_font
        )
        self.name_label.grid(
            row=0,
            column=0,
            columnspan=5,
            padx=PADDING,
            pady=PADDING
        )
        self.name_label.bind("<Button-1>", self.show_name_entry)

        # Name entry - only shows when renaming the group

        self.name_entry = tk.Entry(
            self,
            width=5
        )
        self.name_entry.bind("<KeyPress>", self.key_pressed)

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

        self.name_entry.configure(
            bg=self.colors["BG2"],
            fg=self.colors["HL2"]
        )

        for entry in self.entries:
            entry.refresh_colors(colors)

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


    def show_name_entry(self, event):
        self.name_label.grid_remove()
        self.name_entry.grid(
            row=0,
            column=0,
            columnspan=5,
            padx=PADDING,
            pady=PADDING
        )
        self.name_entry.focus_set()
        self.name_entry.delete(0, tk.END)
        self.name_entry.insert(0, self.name)
        self.name_entry.select_range(start=0, end=tk.END)

    def hide_name_entry(self):
        self.name_entry.grid_remove()
        self.name_label.grid()

    def key_pressed(self, event):
        if event.keysym == "Return":
            new_name = self.name_entry.get()
            if len(new_name) > 0:
                self.master.master.master.rename_group(self.name, new_name)
                self.name = new_name
                self.name_label.configure(text=new_name)
                self.hide_name_entry()
                self.master.master.master.master.bottom_frame.input.focus_set()