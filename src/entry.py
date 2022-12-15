import tkinter as tk
import tkinter.font as tkFont

from math import floor

from colors import get_colors
from constants import *
from data import *

class Entry(tk.Frame):
    def __init__(self, date, time, text, width, height, index, master=None):

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

        self.keys_pressed = {
            "cmd": False,
            "shift": False
        }

        # Variable height

        if len(text) > 100:
            self.height = height + (floor((len(text) - 100) / 5.5))

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

        self.refresh_colors()



    def create_widgets(self):
        self.date_label = tk.Label(
            self, 
            text=self.date,
            font=self.font_bold
        )
        self.date_label.grid(
            row=0, 
            column=0
        )
        self.labels.append(self.date_label)

        self.time_label = tk.Label(
            self, 
            text=self.time,
            font=self.font
        )
        self.time_label.grid(
            row=0, 
            column=2
        )
        self.labels.append(self.time_label)

        self.text_label_var = tk.StringVar(self)
        self.text_label = tk.Label(
            self, 
            font=self.font,
            wraplength=720,
            anchor=tk.NW,
            justify=tk.LEFT,
            width=100,
            textvariable=self.text_label_var
        )
        self.text_label_var.set(self.text)
        self.text_label.grid(
            row=1, 
            column=0, 
            padx=PADDING,
            pady=PADDING,
            columnspan=100
        )
        self.labels.append(self.text_label)



        # Buttons

        self.edit_button = tk.Button(
            self,
            text="edit",
            width=1,
            command=self.edit_pressed
        )
        self.edit_button.grid(
            row=0,
            column=3
        )
        self.buttons.append(self.edit_button)

        self.up_button = tk.Button(
            self,
            text="up",
            width=1,
            command=self.up_pressed
        )
        self.up_button.grid(
            row=0,
            column=4
        )
        self.buttons.append(self.up_button)

        self.down_button = tk.Button(
            self,
            text="down",
            width=1,
            command=self.down_pressed
        )
        self.down_button.grid(
            row=0,
            column=5
        )
        self.buttons.append(self.down_button)

        self.copy_button = tk.Button(
            self,
            text="copy",
            width=2,
            command=self.copy_pressed
        )
        self.copy_button.grid(
            row=0,
            column=6
        )
        self.buttons.append(self.copy_button)

        self.x_button = tk.Button(
            self,
            text="x",
            width=1,
            command=self.x_pressed
        )
        self.x_button.grid(
            row=0,
            column=7
        )
        self.buttons.append(self.x_button)



        # Widgets that only show when "edit" button pressed

        self.edit_box = tk.Text(
            self,
            width=100,
            height=(self.height // 30)
        )

        self.save_button = tk.Button(
            self,
            text="save",
            width=1,
            command=self.edit_save
        )
        self.buttons.append(self.save_button)



    def refresh_colors(self):
        self.colors = get_colors()

        self.configure(
            bg=self.colors["BG1"]
        )

        for label in self.labels:
            label.configure(
                bg=self.colors["BG1"], 
                fg=self.colors["HL2"]
            )

        for button in self.buttons:
            button.configure(
                highlightbackground=self.colors["BG1"]
            )

        self.edit_box.configure(
            bg=self.colors["BG1"],
            fg=self.colors["HL2"]
        )


    # Button handlers

    def edit_pressed(self):
        self.text_label.grid_remove()
        for button in self.buttons:
            button.grid_remove()

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

        self.save_button.grid(
            row=0,
            column=3
        )

    def x_pressed(self):
        remove_entry(self.index)
        self.master.master.master.refresh_entries()

    def up_pressed(self):
        if self.index > 0:
            swap_entry(self.index - 1, self.index)
            self.master.master.master.refresh_entries()

    def down_pressed(self):
        if self.index < len(get_entries()) - 1:
            swap_entry(self.index, self.index + 1)
            self.master.master.master.refresh_entries()

    def copy_pressed(self):
        self.clipboard_clear()
        self.clipboard_append(self.text)



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
        self.save_button.grid_remove()

        # Re-grid the usual Entry widgets
        self.text_label.grid(
            row=1, 
            column=0, 
            padx=PADDING,
            pady=PADDING,
            columnspan=100
        )

        count = 3
        for button in self.buttons:
            button.grid(
                row=0,
                column=count
            )
            count += 1

        self.master.master.master.master.bottom_frame.input.focus_set()



    # Edit selection mode - from pressing cmd+e

    def edit_selected(self, selected):
        if selected:
            self.edit_button.configure(
                highlightbackground=self.colors["HL2"]
            )
        else:
            self.edit_button.configure(
                highlightbackground=self.colors["BG1"]
            )