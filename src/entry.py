import tkinter as tk

from math import floor

from constants import *
from data import *
from entry_menu import EntryMenu
from group_window import GroupWindow

class Entry(tk.Frame):
    def __init__(self, master, date, time, menu, text, 
        width, height, index, font,
        checkbox=False, checked=False, group=None):

        tk.Frame.__init__(
            self,
            master,
            width=width,
            height=height
        )

        # Variables

        self.date = date
        self.time = time
        self.text = text
        self.index = index
        self.width = width
        self.height = height
        self.font = font
        self.group = group

        length = len(self.text)
        newline_count = self.text.count('\n')

        self.group_window = None

        # show a checkbox or not
        self.check_bool = checkbox
        # checkbox is checked or not
        self.checked_bool = checked
        # the checkbox object itself
        self.checkbox = None

        # show the menu or not
        self.menu_bool = menu

        self.keys_pressed = {
            "cmd": False,
            "shift": False
        }

        # Variable height

        # To make sure the Entry is tall enough if there are a 
        # lot of line breaks
        if newline_count > 0:
            avg_line_length = len(self.text) / newline_count
        else:
            avg_line_length = len(self.text)

        if MODE == "fullscreen":
            vh_constant = 9.0
        else:
            vh_constant = 5.6

        if PLATFORM == "Windows":
            if MODE == "fullscreen":
                vh_constant = 6.4
            else:
                vh_constant = 3.09

        # Variable height kicks in after a "limit" of characters
        vh_limit = 60

        newline_offset = newline_count * 5

        if len(text) >= vh_limit:
            # Height is the length of the text divided by a constant
            self.height = height + (floor((length - vh_limit) / vh_constant))
            # plus an offset for any new lines
            self.height += newline_offset
            # and another offset for if there are multiple newlines that are really short
            if newline_count > 5:
                self.height += floor(400 / avg_line_length)

        self.configure(height=self.height)

        # Arrays for easy widget configuration

        self.labels = []
        self.buttons = []

        # Get parent "Entries" object for later use

        self.get_entries_obj()

        self.create_widgets()



    def create_widgets(self):

        # Checkbox

        # for gridding the text label next to the checkbox
        column_var = 0

        if self.check_bool:
            self.checkbox_var = tk.IntVar()
            if self.checked_bool:
                self.checkbox_var.set(1)
            self.checkbox = tk.Checkbutton(
                self,
                width=2,
                height=1,
                anchor=tk.NW,
                variable=self.checkbox_var,
                command=self.checkbox_pressed
            )
            self.checkbox.grid(
                row=1, 
                column=0, 
                padx=PADDING
            )
            column_var = 1


        # Entry menu - contains all the labels and buttons at the top.

        self.entry_menu = EntryMenu(
            self,
            self.date,
            self.time,
            self.check_bool,
            self.checked_bool, 
            self.font
        )
        if self.menu_bool:
            self.entry_menu.grid(row=0, column=0, columnspan=2)


        # Text label - shows the actual text of the Entry

        self.text_label_var = tk.StringVar(self)

        if self.check_bool:
            self.text_label_wrap_length = self.width - 80
        else:
            self.text_label_wrap_length = self.width - 40

        self.text_label = tk.Label(
            self, 
            font=self.font,
            wraplength=self.text_label_wrap_length,
            anchor=tk.NW,
            justify=tk.LEFT,
            width=200,
            textvariable=self.text_label_var
        )
        self.text_label_var.set(self.text)
        self.text_label.grid(
            row=1, 
            column=column_var, 
            padx=PADDING,
            pady=PADDING,
            columnspan=200,
            rowspan=3
        )
        self.labels.append(self.text_label)


        # Edit box - only shows in edit mode

        self.edit_box = tk.Text(
            self,
            width=100,
            height=(self.height // 30)
        )
        if PLATFORM == "Windows":
            self.edit_box.configure(width=90)



    def refresh_colors(self, colors):
        self.colors = colors

        main_fg = self.colors["HL2"]
        if self.checked_bool:
            main_fg = self.colors["HL1"]

        self.entry_menu.refresh_colors(colors, main_fg)

        self.text_label.configure(
            bg=self.colors["BG1"], 
            fg=main_fg
        )

        self.configure(
            bg=self.colors["BG1"]
        )
        
        if self.checkbox:
            self.checkbox.configure(
                bg=self.colors["BG1"],
                highlightbackground=self.colors["BG1"]
            )

        self.edit_box.configure(
            bg=self.colors["BG1"],
            fg=main_fg
        )

        if self.group_window:
            self.group_window.refresh_colors(colors)



    # Edit mode button pressed

    def edit_pressed(self):
        self.entry_menu.edit_pressed()

        self.text_label.grid_remove()

        self.edit_box.grid(
            row=1, 
            column=0, 
            padx=PADDING,
            pady=PADDING,
            columnspan=100
        )

        self.edit_box.insert("1.0", self.text_label_var.get())
        self.edit_box.delete("end - 1 chars") # remove newline
        self.edit_box.focus_set()

        self.edit_box.bind("<KeyPress>", self.edit_box_key_pressed)
        self.edit_box.bind("<KeyRelease>", self.edit_box_key_released)

    # Edit mode save button handler

    def edit_save(self):
        # Change internally stored text
        self.text = self.edit_box.get("1.0", "end")

        # Remove newline from the end if there is one
        if self.text[-1] == '\n':
            self.text = self.text[:-1]

        # Change text label
        self.text_label_var.set(self.text)
        
        # Empty the edit box
        self.edit_box.delete("1.0", "end")

        # Save to the array in data.py
        remove_entry(self.index)
        insert_entry(self.index, self.text)

        # Remove edit box and save button
        self.edit_box.grid_remove()

        # Re-grid the usual Entry widgets
        self.text_label.grid()
        self.entry_menu.edit_save()

        if self.check_bool:
            self.checkbox.grid()

        self.entries_obj.master.bottom_frame.input.focus_set()



    # Edit box key handlers

    def edit_box_key_pressed(self, event):
        if "Meta" in event.keysym:
            self.keys_pressed["cmd"] = True
        if "Shift" in event.keysym:
            self.keys_pressed["shift"] = True

        if ("Return" in event.keysym 
            and self.keys_pressed["shift"] == False):
            self.edit_save()

    def edit_box_key_released(self, event):
        if "Meta" in event.keysym:
            self.keys_pressed["cmd"] = False
        if "Shift" in event.keysym:
            self.keys_pressed["shift"] = False



    # Edit selection mode - from pressing cmd+e

    def edit_selected(self, selected):
        if selected:
            self.entry_menu.set_selected(True)
        else:
            self.entry_menu.set_selected(False)


    # Other button handlers

    def x_pressed(self):
        remove_entry(self.index)
        self.entries_obj.refresh_entries()

    def up_pressed(self):
        move_entry(self.group, self.text, dir="up")
        self.entries_obj.refresh_entries()

    def down_pressed(self):
        move_entry(self.group, self.text, dir="down")
        self.entries_obj.refresh_entries()

    def copy_pressed(self):
        self.clipboard_clear()
        self.clipboard_append(self.text)

    def top_pressed(self):
        move_entry(self.group, self.text, dir="top")
        self.entries_obj.refresh_entries()

    def bottom_pressed(self):
        move_entry(self.group, self.text, dir="bottom")
        self.entries_obj.refresh_entries()


    def group_pressed(self):
        group_names = self.get_group_names()
        self.group_window = GroupWindow(self, group_names)
        self.group_window.refresh_colors(self.colors)

        # If there's at least one group, select it in the listbox
        if len(self.group_window.list_var.get()) > 0:
            self.group_window.group_list.selection_set(0, 0)
            # act as though the selection were "clicked"
            # self.group_window.on_click()

    def checkbox_pressed(self):
        # Move entries to bottom when checked
        if self.checkbox_var.get() == 1:
            for entry in self.entries_obj.entries_data:
                if entry["index"] == self.index:
                    entry["checked"] = True
                    break
            self.bottom_pressed()

        # Move back to top when unchecked
        else:
            self.entries_obj.entries_data[self.index]["checked"] = False
            self.top_pressed()

    

    # Functions that do nothing but pass on to the Entries object

    # (just so I don't have to call 
    # self.master.master.master.master.master etc etc etc 
    # from the group window)

    def add_group(self, name):
        self.entries_obj.add_group(name)

    def get_group_names(self):
        return self.entries_obj.get_group_names()

    def move_group(self, name, dir):
        self.entries_obj.move_group(name, dir)

    def move_to_group(self, group_name):
        move_entry_to_group(self.index, self.group, group_name)
        self.entries_obj.refresh_entries()

    def delete_group(self, group_name):
        if self.group:
            self.master.master.master.master.delete_group(group_name)
        else:
            self.master.master.master.delete_group(group_name)


    # Utility for getting access to the Entries object through the master chain

    def get_entries_obj(self):
        if self.group:
            self.entries_obj = self.master.master.master.master
        else:
            self.entries_obj = self.master.master.master