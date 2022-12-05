import tkinter as tk

from constants import *
from data import entries
from entry import Entry

class Entries(tk.Frame):
    def __init__(self, width, height, bg, master=None):
        tk.Frame.__init__(self, master, width=width, height=height, bg=bg)
        self.create_widgets()

    def create_widgets(self):
        self.entries = []
        
        self.refresh_entries()

    def refresh_entries(self):
        for entry in self.entries:
            entry.grid_forget()

        self.entries.clear()

        for count in range(len(entries)):
            self.entries.append(Entry(
                date=entries[count]["date"],
                text=entries[count]["text"],
                width=(WIDTH - (PADDING * 2)),
                height=80,
                bg="white",
                master=self
            ))
            self.entries[count].grid_propagate(0)
            self.entries[count].grid(row=count, column=0,
                padx=PADDING, pady=PADDING)