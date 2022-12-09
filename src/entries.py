import tkinter as tk

from constants import *
from colors import get_colors
from data import get_entries
from entry import Entry

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

        self.create_widgets()

        self.refresh_colors()

    def refresh_colors(self):
        self.colors = get_colors()

        self.canvas.configure(bg=self.colors["HL1"])

        self.scrollbar.configure(
            bg=self.colors["BG2"],
            highlightbackground=self.colors["HL1"],
            highlightcolor=self.colors["HL1"]
        )

        for entry in self.entries:
            entry.configure(bg=self.colors["BG2"])


    def scroll_config(self, event=None):
        self.canvas.configure(
            scrollregion=self.canvas.bbox("all"),
            width=self.width - (PADDING * 2),
            height=self.height
        )

    def create_widgets(self):
        self.canvas = tk.Canvas(self)
        self.scroll_config()
        self.container = tk.Frame(
            self.canvas)
        self.scrollbar = tk.Scrollbar(self,
            orient="vertical",
            command=self.canvas.yview,
            width=20,
            takefocus=0
        )
        self.canvas.configure(
            yscrollcommand=self.scrollbar.set)

        self.canvas.grid(row=0, column=0)
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
        
        self.refresh_entries()

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
                width=(WIDTH - (PADDING * 6)),
                height=ENTRY_HEIGHT,
                master=self.container,
                index=count
            ))
            self.entries[count].grid_propagate(0)
            self.entries[count].grid(
                row=count, 
                column=0,
                padx=PADDING, 
                pady=PADDING,
                sticky=tk.W
            )