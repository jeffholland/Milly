import tkinter as tk

from constants import *
from data import get_entries
from entry import Entry
# from subentry import SubEntry

class Entries(tk.Frame):
    def __init__(self, width, height, master=None):
        tk.Frame.__init__(
            self, 
            master, 
            width=width, 
            height=height)
        self.width = width
        self.height = height
        self.canvas_object_ids = []

        self.entry_width = self.width - (PADDING * 6)

        self.create_widgets()

        self.refresh_colors()



    def create_widgets(self):
        self.canvas = tk.Canvas(self)
        self.scrollbar = tk.Scrollbar(self,
            orient="vertical",
            command=self.canvas.yview,
            width=20,
            takefocus=0
        )
        self.canvas.configure(
            yscrollcommand=self.scrollbar.set
        )
        self.container = tk.Frame(
            self.canvas
        )
        self.canvas.grid(row=0, column=0)
        self.scroll_config()
        self.scrollbar.grid(
            row=0, 
            column=1, 
            sticky="ns"
        )

        self.canvas_object_ids.append(
            self.canvas.create_window(
                (0,0),
                window=self.container,
                anchor='nw'
            )
        )

        self.container.bind("<Configure>", self.scroll_config)
        self.container.bind("<Motion>", self.scroll_config)

        # Contains the Entry objects
        self.entries = []

        # Contains the array of dicts sourced from data.py
        self.entries_data = []

        # Contains the SubEntry objects
        # self.sub_entries = []
        
        self.refresh_entries()

    def refresh_colors(self):
        self.colors = self.master.colors_obj.get_colors()

        self.canvas.configure(bg=self.colors["HL1"])

        self.scrollbar.configure(
            bg=self.colors["BG2"],
            highlightbackground=self.colors["HL1"],
            highlightcolor=self.colors["HL1"]
        )

        for entry in self.entries:
            entry.refresh_colors()

        self.container.configure(bg=self.colors["HL1"])



    def refresh_entries(self):
        self.entries_data = get_entries()

        for entry in self.entries:
            entry.grid_forget()

        self.entries.clear()

        for count in range(len(self.entries_data)):
            self.entries.append(Entry(
                date=self.entries_data[count]["date"],
                time=self.entries_data[count]["time"],
                text=self.entries_data[count]["text"],
                width=self.entry_width,
                height=ENTRY_HEIGHT,
                master=self.container,
                index=count
            ))
            # self.sub_entries.append(SubEntry(
            #     date=self.entries_data[count]["date"],
            #     time=self.entries_data[count]["time"],
            #     text=self.entries_data[count]["text"],
            #     width=self.entry_width,
            #     height=ENTRY_HEIGHT,
            #     master=self.container,
            #     index=count
            # ))
            self.entries[count].grid_propagate(0)
            self.entries[count].grid(
                row=count, 
                column=0,
                padx=PADDING, 
                pady=PADDING
            )
            # self.sub_entries[count].grid_propagate(0)
            # self.sub_entries[count].grid(
            #     row=count + len(self.entries), 
            #     column=0,
            #     padx=PADDING, 
            #     pady=PADDING
            # )



    def scroll_config(self, event=None):
        self.canvas.configure(
            scrollregion=self.canvas.bbox("all"),
            width=self.width - 25,
            height=self.height
        )