import tkinter as tk

from constants import *
from data import get_entries
from entry import Entry
from export import ExportWindow

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

        self.show_checkboxes = False

        self.create_widgets()

        self.refresh_colors()



    def refresh_entries(self):
        self.entries_data = get_entries()

        for entry in self.entries:
            entry.grid_forget()

        self.entries.clear()

        for count in range(len(self.entries_data)):
            try:
                checked_bool = self.entries_data[count]["checked"]
            except KeyError:
                checked_bool = False

            self.entries.append(Entry(
                date=self.entries_data[count]["date"],
                time=self.entries_data[count]["time"],
                text=self.entries_data[count]["text"],
                width=self.entry_width,
                height=ENTRY_HEIGHT,
                master=self.container,
                index=count,
                checkbox=self.show_checkboxes,
                checked=checked_bool
            ))
            self.entries[count].grid_propagate(0)
            self.entries[count].grid(
                row=count, 
                column=0,
                padx=PADDING, 
                pady=PADDING
            )



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

        # Contains a list of Entry objects
        self.entries = []

        # Contains a list of dicts sourced from data.py
        self.entries_data = []

        # Contains a filtered list of Entry objects
        self.filtered_entries = []

        # Contains a filtered list of dicts
        self.filtered_entries_data = []
        
        self.refresh_entries()


        # Export window

        self.export_window = ExportWindow(self)
        self.export_window.window.withdraw()



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



    def filter_entries(self, filter, case_sensitive=False):
        for entry in self.entries:
            entry.grid_forget()

        for entry in self.filtered_entries:
            entry.grid_forget()

        self.filtered_entries.clear()
        self.filtered_entries_data.clear()

        for data in self.entries_data:
            if case_sensitive:
                if filter in data["text"]:
                    self.filtered_entries_data.append(data)
            else:
                if filter.lower() in data["text"].lower():
                    self.filtered_entries_data.append(data)
        
        for count in range(len(self.filtered_entries_data)):
            self.filtered_entries.append(
                Entry(
                    date=self.filtered_entries_data[count]["date"],
                    time=self.filtered_entries_data[count]["time"],
                    text=self.filtered_entries_data[count]["text"],
                    width=self.entry_width,
                    height=ENTRY_HEIGHT,
                    master=self.container,
                    index=count
                )
            )
            self.filtered_entries[count].grid_propagate(0)
            self.filtered_entries[count].grid(
                row=count, 
                column=0,
                padx=PADDING, 
                pady=PADDING
            )

    def remove_filter(self):
        for entry in self.filtered_entries:
            entry.grid_forget()

        self.refresh_entries()


    def scroll_config(self, event=None):
        self.canvas.configure(
            scrollregion=self.canvas.bbox("all"),
            width=self.width - 25,
            height=self.height
        )


    def export(self):
        self.export_window.window.deiconify()