import tkinter as tk
import tkinter.font as tkFont

from constants import *
from data import *
from entry import Entry
from export import ExportWindow
from group import Group

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

        self.entry_width = self.width - (PADDING * 2)

        # Booleans for showing and hiding entry features
        self.show_checkboxes = False
        self.show_dates = False
        self.show_times = False
        self.show_menu = False

        self.colors = None

        self.font = tkFont.Font(self, family="Helvetica", size=14)


        # Initialization

        # List of Entry objects
        self.ungrouped_entries = []

        # List containing all ungrouped entry data
        self.ungrouped_entries_data = []

        # List of Group objects
        self.groups = []

        # List containing all Group data
        self.groups_data = []

        # List of group names
        self.group_names = []

        # Contains a filtered list of Group objects
        self.filtered_groups = []

        # Contains a filtered list of Group data
        self.filtered_groups_data = []

        # Contains a filtered list of Entry objects
        self.filtered_entries = []

        # Contains a filtered list of Entries data
        self.filtered_entries_data = []

        # Indexes every entry
        self.index_count = 0

        self.create_widgets()



    # IMPORTANT: this is the function where the entries get
    # put on the screen.

    def refresh_entries(self, refresh_data=True):

        # 1. Clear all entries and groups from the screen

        self.clear_entries()

        # 2. Get the data from the data.py repo

        if refresh_data:
            self.get_entry_data()

        # 4. Create group objects and display them on the screen

        self.create_groups()

        # 5. Create ungrouped entries and display them on the screen

        self.create_ungrouped_entries()

        # 6. Refresh colors

        if self.colors:
            self.refresh_colors(self.colors)


    def clear_entries(self):
        for entry in self.ungrouped_entries:
            entry.grid_forget()
        for group in self.groups:
            group.grid_forget()

        self.ungrouped_entries.clear()
        self.groups.clear()
        self.group_names.clear()


    def get_entry_data(self):

        # Get all saved data as a dictionary

        data = get_data()

        # Get all group data into an array of dicts

        try:
            self.groups_data = data["groups"]
        except KeyError:
            data["groups"] = []
            self.groups_data = []

        # Get all ungrouped entries data into an array of dicts

        try:
            self.ungrouped_entries_data = data["entries"]
        except KeyError:
            data["entries"] = []
            self.ungrouped_entries_data = []

        # Get group names as an array

        for group in self.groups_data:
            self.group_names.append(group["name"])



    def create_groups(self):
        count = 0

        for group in self.groups_data:
            name = group["name"]
            entries = group["entries"]
        
            self.groups.append(Group(
                self.container,
                width=self.entry_width,
                entry_height=ENTRY_HEIGHT,
                entries_data=entries,
                name=name,
                font=self.font,
                show_dates=self.show_dates,
                show_times=self.show_times
            ))

            self.groups[count].grid_propagate(0)
            self.groups[count].grid(
                row=count, 
                column=0,
                padx=PADDING,
                pady=PADDING
            )

            # Update count
            count += 1

    def refresh_group_names(self):
        self.group_names = get_group_names()

    def create_ungrouped_entries(self):

        count = 0

        for entry in self.ungrouped_entries_data:
            try:
                checked_bool = self.ungrouped_entries_data[count]["checked"]
            except KeyError:
                self.ungrouped_entries_data[count]["checked"] = False
                checked_bool = self.ungrouped_entries_data[count]["checked"]

            entry_date = None
            if self.show_dates:
                entry_date = entry["date"]
            entry_time = None
            if self.show_times:
                entry_time = entry["time"]

            text = entry["text"]

            try:
                widgets = entry["widgets"]
            except KeyError:
                widgets = []

            self.ungrouped_entries.append(Entry(
                self.container,
                date=entry_date,
                time=entry_time,
                menu=self.show_menu,
                text=text,
                width=self.entry_width,
                height=ENTRY_HEIGHT,
                index=count,
                font=self.font,
                checkbox=self.show_checkboxes,
                checked=checked_bool,
                widgets=widgets
            ))
            self.ungrouped_entries[count].grid_propagate(0)
            entry_row = count + len(self.groups)
            self.ungrouped_entries[count].grid(
                row=entry_row, 
                column=0,
                padx=PADDING, 
                pady=PADDING
            )

            count += 1



    def create_widgets(self):
        self.canvas = tk.Canvas(self)
        self.container = tk.Frame(
            self.canvas
        )
        self.canvas.grid(row=0, column=0)
        self.scroll_config()

        self.canvas_object_ids.append(
            self.canvas.create_window(
                (0,0),
                window=self.container,
                anchor='nw'
            )
        )

        self.container.bind("<Configure>", self.scroll_config)
        self.container.bind("<Motion>", self.scroll_config)
        
        self.refresh_entries()


        # Export window

        self.export_window = ExportWindow(self)
        self.export_window.window.withdraw()


        # Scroll with mouse wheel

        self.canvas.bind_all("<MouseWheel>", self.on_mouse_wheel)

    
    def on_mouse_wheel(self, event):
        if PLATFORM == "Windows":
            self.canvas.yview_scroll(-1*(event.delta/120), "units")
        else:
            self.canvas.yview_scroll(-1*(event.delta), "units")


    def scroll_config(self, event=None):
        self.canvas.configure(
            scrollregion=self.canvas.bbox("all"),
            width=self.width,
            height=self.height
        )



    def refresh_colors(self, colors):
        self.colors = colors

        self.container.configure(bg=self.colors["HL1"])

        self.canvas.configure(bg=self.colors["HL1"])

        for group in self.groups:
            group.refresh_colors(colors)

        for entry in self.ungrouped_entries:
            entry.refresh_colors(colors)

        self.export_window.refresh_colors(colors)



    def filter_entries(self, filter, case_sensitive=False):
        for group in self.groups:
            group.grid_remove()

        for group in self.filtered_groups:
            group.grid_remove()

        for entry in self.ungrouped_entries:
            entry.grid_remove()

        for entry in self.filtered_entries:
            entry.grid_remove()

        self.filtered_groups.clear()
        self.filtered_groups_data.clear()
        self.filtered_entries.clear()
        self.filtered_entries_data.clear()

        # Search groups
        count = -1
        for group in self.groups_data:
            added_group = False
            for data in group["entries"]:
                if filter.lower() in data["text"].lower():
                    if added_group:
                        self.filtered_groups_data[count]["entries"].append(data)
                    else:
                        name = group["name"]
                        self.filtered_groups_data.append(
                            {
                                "name": name,
                                "entries": [data]
                            }
                        )
                        added_group = True
                        count += 1

        # Search ungrouped entries
        for data in self.ungrouped_entries_data:
            if case_sensitive:
                if filter in data["text"]:
                    self.filtered_entries_data.append(data)
            else:
                if filter.lower() in data["text"].lower():
                    self.filtered_entries_data.append(data)

        # Create and grid filtered group objects
        count = 0
        for group in self.filtered_groups_data:
            self.filtered_groups.append(
                Group(
                    self.container,
                    width=self.entry_width,
                    entry_height=ENTRY_HEIGHT,
                    entries_data=group["entries"],
                    name=group["name"],
                    font=self.font,
                    show_dates=self.show_dates,
                    show_times=self.show_times
                )
            )
            self.filtered_groups[count].grid_propagate(0)
            self.filtered_groups[count].grid(
                row=count, 
                column=0,
                padx=PADDING, 
                pady=PADDING
            )
            self.filtered_groups[count].refresh_colors(self.colors)
            count += 1

        # Create and grid filtered ungrouped entry objects
        count = 0
        for entry in self.filtered_entries_data:
            self.filtered_entries.append(
                Entry(
                    date=entry["date"],
                    time=entry["time"],
                    text=entry["text"],
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
            count += 1

    def remove_filter(self):
        for group in self.filtered_groups:
            group.grid_forget()
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



    # Group functions

    def get_group_names(self):
        return self.group_names

    def add_group(self, name):
        self.group_names.append(name)
        add_group(name)
        self.refresh_entries()

    def delete_group(self, name):
        for group in self.groups:
            if group.name == name:
                group.delete()
                try:
                    self.group_names.remove(group.name)
                    self.groups.remove(group)
                except ValueError:
                    pass
                break

        for entry in self.ungrouped_entries_data:
            if entry["group"] == name:
                entry["group"] = "None"

        self.refresh_entries()

    def get_group(self, name):
        for group in self.groups:
            if group.name == name:
                return group

    # def set_group(self, index, name):
    #     count = 0
    #     for entry in self.ungrouped_entries_data:
    #         if entry["index"] == index:
    #             data_index = count
    #             break
    #         count += 1
    #     self.ungrouped_entries_data[data_index]["group"] = name