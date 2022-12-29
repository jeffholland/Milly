import tkinter as tk

from constants import *

class EntryMenu(tk.Frame):
    def __init__(self, master, date, time, check_bool, checked_bool, 
        font):

        tk.Frame.__init__(self, master)
        self.master = master

        # Passing down variables
        self.date = date
        self.time = time
        self.check_bool = check_bool
        self.checked_bool = checked_bool
        self.font = font

        self.labels = []
        self.buttons = []

        self.create_widgets()



    def create_widgets(self):
        self.date_label = tk.Label(
            self, 
            text=self.date,
            font=self.font
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
            command=self.master.edit_pressed
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
            command=self.master.up_pressed
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
            command=self.master.down_pressed
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
            command=self.master.top_pressed
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
            command=self.master.bottom_pressed
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
            command=self.master.copy_pressed
        )
        self.copy_button.grid(
            row=0,
            column=8
        )
        self.buttons.append(self.copy_button)

        self.group_button = tk.Button(
            self,
            text="group",
            width=self.button_width,
            command=self.master.group_pressed
        )
        self.group_button.grid(
            row=0,
            column=9
        )
        self.buttons.append(self.group_button)

        if PLATFORM != "Windows":
            self.copy_button.configure(width=self.button_width * 2)

        self.x_button = tk.Button(
            self,
            text="x",
            width=self.button_width,
            command=self.master.x_pressed
        )
        self.x_button.grid(
            row=0,
            column=10
        )
        self.buttons.append(self.x_button)
        if PLATFORM == "Windows":
            self.x_button.configure(width=1)

        # only shows in edit mode

        self.save_button = tk.Button(
            self,
            text="save",
            width=self.button_width,
            command=self.master.edit_save
        )
        self.buttons.append(self.save_button)


    def refresh_colors(self, colors, main_fg):
        self.colors = colors

        self.configure(bg=self.colors["BG1"])

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



    def edit_pressed(self):
        for button in self.buttons:
            button.grid_remove()

        self.save_button.grid(
            row=0,
            column=3
        )

    def edit_save(self):

        self.save_button.grid_remove()
        for button in self.buttons:
            # Don't re-grid the save button
            if button.cget("text") == "save":
                continue

            button.grid()



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