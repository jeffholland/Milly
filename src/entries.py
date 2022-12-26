import tkinter as tk
import tkinter.font as tkFont

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

        # Booleans for showing and hiding entry features
        self.show_checkboxes = False
        self.show_dates = False
        self.show_times = False
        self.show_menu = False

        self.colors = None

        self.font = tkFont.Font(self, family="Helvetica", size=14)

        self.create_widgets()



    # IMPORTANT: this is the function where the entries get
    # put on the screen.

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

            entry_date = None
            if self.show_dates:
                entry_date = self.entries_data[count]["date"]
            entry_time = None
            if self.show_times:
                entry_time = self.entries_data[count]["time"]

            self.entries.append(Entry(
                self.container,
                date=entry_date,
                time=entry_time,
                menu=self.show_menu,
                text=self.entries_data[count]["text"],
                width=self.entry_width,
                height=ENTRY_HEIGHT,
                index=count,
                font=self.font,
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
        if self.colors:
            self.refresh_colors(self.colors)



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


        # Scroll with mouse wheel

        self.canvas.bind_all("<MouseWheel>", self.on_mouse_wheel)

    
    def on_mouse_wheel(self, event):
        self.canvas.yview_scroll(-1*(event.delta), "units")


    def scroll_config(self, event=None):
        self.canvas.configure(
            scrollregion=self.canvas.bbox("all"),
            width=self.width - 25,
            height=self.height
        )



    def refresh_colors(self, colors):
        self.colors = colors

        self.container.configure(bg=self.colors["HL1"])

        self.canvas.configure(bg=self.colors["HL1"])

        self.scrollbar.configure(
            bg=self.colors["BG2"],
            highlightbackground=self.colors["HL1"],
            highlightcolor=self.colors["HL1"]
        )

        for entry in self.entries:
            entry.refresh_colors(colors)

        self.export_window.refresh_colors(colors)



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
            self.filtered_entries[count].refresh_colors(self.colors)

    def remove_filter(self):
        for entry in self.filtered_entries:
            entry.grid_forget()

        self.refresh_entries()


    def export(self):
        self.export_window.window.deiconify()
        self.export_window.filename_entry.focus_set()

    def set_font(self, font):
        self.font = font
        self.refresh_entries()

    def set_show_dates(self, show_dates):
        self.show_dates = show_dates
        if show_dates:
            self.export_window.dates_button.configure(
                state=tk.NORMAL
            )
        else:
            self.export_window.dates_button.configure(
                state=tk.DISABLED
            )
        self.refresh_entries()

    def set_show_times(self, show_times):
        self.show_times = show_times
        if show_times:
            self.export_window.times_button.configure(
                state=tk.NORMAL
            )
        else:
            self.export_window.times_button.configure(
                state=tk.DISABLED
            )
        self.refresh_entries()
