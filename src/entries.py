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

        # List of dicts containing all Entry data
        self.ungrouped_entries_data = []

        # List of Group objects
        self.groups = []

        # List of dicts containing all Group data
        self.groups_data = []

        # List of group names
        self.group_names = []

        # Contains a filtered list of Entry objects (for cmd+f search)
        self.filtered_entries = []

        # Contains a filtered list of dicts (for cmd+f search)
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
            for group in data["groups"]:
                self.group_names.append(group)
            # print(f"group: {self.groups_data}\n")
            # print(f"group names: {self.group_names}\n")
        except KeyError:
            self.groups_data = []

        # Get all ungrouped entries data into an array of dicts

        try:
            self.ungrouped_entries_data = data["entries"]
            # print(f"ungrouped: {self.ungrouped_entries_data}\n")
        except KeyError:
            self.ungrouped_entries_data = []



    def create_groups(self):
        count = 0

        for name in self.group_names:

            group_data = self.groups_data[name]
        
            self.groups.append(Group(
                self.container,
                width=self.entry_width,
                entry_height=ENTRY_HEIGHT,
                entries_data=group_data,
                name=name,
                font=self.font
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
                entry_id = entry["id"]
            except KeyError:
                entry["id"] = hashlib.sha256(str.encode(text)).hexdigest()
                entry_id = entry["id"]

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
                id=entry_id,
                checkbox=self.show_checkboxes,
                checked=checked_bool
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
        for entry in self.ungrouped_entries:
            entry.grid_forget()

        for entry in self.filtered_entries:
            entry.grid_forget()

        self.filtered_entries.clear()
        self.filtered_entries_data.clear()

        for data in self.ungrouped_entries_data:
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

    # def rename_group(self, old_name, new_name):
    #     for entry in self.ungrouped_entries_data:
    #         if entry["group"] == old_name:
    #             entry["group"] = new_name

    # def move_group(self, name, dir):
    #     count = 0
    #     for group_name in self.group_names:
    #         if group_name == name:
    #             if dir == "up":
    #                 if count > 0:
    #                     self.swap_groups(count, count - 1)

    #             if dir == "down":
    #                 if count < len(self.group_names) - 1:
    #                     self.swap_groups(count, count + 1)
                
    #             break

    #         count += 1
    #     self.refresh_entries(refresh_data=False)

    # def swap_groups(self, pos1, pos2):
    #     self.group_names[pos1], self.group_names[pos2] = self.group_names[pos2], self.group_names[pos1]