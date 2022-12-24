import tkinter as tk
import tkinter.font as tkFont

from math import floor

from constants import *
from data import *

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

        wraplength = 100
        newline_count = self.text.count('\n')

        print(f"Number of characters: {len(self.text)}")
        print(f"Number of lines at {wraplength} characters per line: {floor(len(self.text) / wraplength)}")
        print(f"Number of times a line break appears: {newline_count}")

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
            newline_offset = floor(newline_count * 2.5)
            self.height = self.height + newline_offset
            self.configure(height=self.height)

        print(f"Actual window height: {self.height}")

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

        if self.check_bool:
            self.date_label.grid_configure(
                columnspan=2
            )

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


        # Buttons

        self.button_width = 1
        if PLATFORM == "Windows":
            self.button_width = 4

        self.edit_button = tk.Button(
            self,
            text="edit",
            width=self.button_width,
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
            width=self.button_width,
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
            width=self.button_width,
            command=self.down_pressed
        )
        self.down_button.grid(
            row=0,
            column=5
        )
        self.buttons.append(self.down_button)

        self.top_button = tk.Button(
            self,
            text="top",
            width=self.button_width,
            command=self.top_pressed
        )
        self.top_button.grid(
            row=0,
            column=6
        )
        self.buttons.append(self.top_button)

        self.bottom_button = tk.Button(
            self,
            text="last",
            width=self.button_width,
            command=self.bottom_pressed
        )
        self.bottom_button.grid(
            row=0,
            column=7
        )
        self.buttons.append(self.bottom_button)

        self.copy_button = tk.Button(
            self,
            text="copy",
            width=self.button_width,
            command=self.copy_pressed
        )
        self.copy_button.grid(
            row=0,
            column=8
        )
        self.buttons.append(self.copy_button)

        if PLATFORM != "Windows":
            self.copy_button.configure(width=self.button_width * 2)

        self.x_button = tk.Button(
            self,
            text="x",
            width=self.button_width,
            command=self.x_pressed
        )
        self.x_button.grid(
            row=0,
            column=9
        )
        self.buttons.append(self.x_button)
        if PLATFORM == "Windows":
            self.x_button.configure(width=1)

        # only shows in edit mode

        self.save_button = tk.Button(
            self,
            text="save",
            width=self.button_width,
            command=self.edit_save
        )
        self.buttons.append(self.save_button)


        # Text label - shows the actual text of the Entry

        self.text_label_var = tk.StringVar(self)

        if self.check_bool:
            self.text_label_wrap_length = self.width - 80
        else:
            self.text_label_wrap_length = self.width - 40
        
        print(f"Actual wrap length: {self.text_label_wrap_length}")

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

        for label in self.labels:
            label.configure(
                bg=self.colors["BG1"], 
                fg=main_fg
            )

        for button in self.buttons:
            button.configure(
                highlightbackground=self.colors["BG1"]
            )
            if PLATFORM == "Windows":
                button.configure(
                    bg=self.colors["BG2"],
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
        # self.entry_menu.edit_pressed()
        
        for button in self.buttons:
            button.grid_remove()

        self.save_button.grid(
            row=0,
            column=3
        )

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

        self.save_button.grid_remove()
        for button in self.buttons:
            # Don't re-grid the save button
            if button.cget("text") == "save":
                continue

            button.grid()

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
            self.set_selected(True)
        else:
            self.set_selected(False)



    def set_selected(self, selected):

        if selected:
            if PLATFORM == "Windows":
                self.edit_button.configure(
                    bg=self.colors["HL2"],
                    fg=self.colors["BG1"]
                )
            else:
                self.edit_button.configure(
                    highlightbackground=self.colors["HL2"]
                )
        else:
            if PLATFORM == "Windows":
                self.edit_button.configure(
                    bg=self.colors["BG2"],
                    fg=self.colors["HL2"]
                )
            else:
                self.edit_button.configure(
                    highlightbackground=self.colors["BG1"]
                )
            self.update_idletasks()


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