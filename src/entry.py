import tkinter as tk
import tkinter.font as tkFont

from math import floor

from constants import *
from data import *
from entry_menu import EntryMenu

class Entry(tk.Frame):
    def __init__(self, date, time, text, width, height, index, 
        master=None, checkbox=False, checked=False):

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

        # include a checkbox or not
        self.check_bool = checkbox
        # checkbox is checked or not
        self.checked_bool = checked
        # the checkbox object itself
        self.checkbox = None

        self.keys_pressed = {
            "cmd": False,
            "shift": False
        }

        # Variable height
        # (need to find a way to do this that doesn't keep breaking)

        if MODE == "fullscreen":
            vh_constant = 9.0
        else:
            vh_constant = 5.36
        vh_limit = 100

        if PLATFORM == "Windows":
            if MODE == "fullscreen":
                vh_constant = 6.4
            else:
                vh_constant = 3.09
            vh_limit = 60

        if len(text) > vh_limit:
            self.height = height + (floor((len(text) - vh_limit) / vh_constant))

            self.configure(height=self.height)

        # Font

        self.font = tkFont.Font(
            family=ENTRY_FONT_FAMILY, 
            size=ENTRY_FONT_SIZE
        )
        self.font_bold = tkFont.Font(
            family=ENTRY_FONT_FAMILY, 
            size=ENTRY_FONT_SIZE, 
            weight="bold"
        )

        # Arrays for easy widget configuration

        self.labels = []
        self.buttons = []

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
            self.font, 
            self.font_bold
        )
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
            columnspan=200
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

        self.master.master.master.master.bottom_frame.input.focus_set()



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
        self.master.master.master.refresh_entries()

    def up_pressed(self):
        if self.index > 0:
            swap_entry(self.index - 1, self.index)
            self.master.master.master.refresh_entries()

    def down_pressed(self):
        if self.index < get_num_entries() - 1:
            swap_entry(self.index, self.index + 1)
            self.master.master.master.refresh_entries()

    def copy_pressed(self):
        self.clipboard_clear()
        self.clipboard_append(self.text)

    def top_pressed(self):
        if self.index > 0:
            move_entry(self.index, 0)
            self.master.master.master.refresh_entries()

    def bottom_pressed(self):
        if self.index < get_num_entries() - 1:
            move_entry(self.index, get_num_entries() - 1)
            self.master.master.master.refresh_entries()

    def checkbox_pressed(self):
        # Move entries to bottom when checked
        if self.checkbox_var.get() == 1:
            self.master.master.master.entries_data[self.index]["checked"] = True
            self.bottom_pressed()

        # Move back to top when unchecked
        else:
            self.master.master.master.entries_data[self.index]["checked"] = False
            self.top_pressed()