import tkinter as tk
import tkinter.font as tkFont

from constants import *

class GroupMenu(tk.Frame):
    def __init__(self, master, name, num_entries):

        tk.Frame.__init__(self, master)
        self.master = master

        self.name = name

        self.title_font = tkFont.Font(self, family="Helvetica", size=20)

        self.buttons = []

        self.create_widgets()

    def create_widgets(self):

        # Name label

        self.name_label = tk.Label(
            self,
            text=self.name,
            font=self.title_font
        )
        self.name_label.grid(
            row=0,
            column=0,
            padx=PADDING,
            pady=PADDING
        )
        self.name_label.bind("<Button-1>", self.show_name_entry)

        # Up button
        self.up_button = tk.Button(
            self,
            text="↑",
            width=1,
            command=self.up_pressed
        )
        self.up_button.grid(
            row=0,
            column=1,
            sticky=tk.NE
        )
        self.buttons.append(self.up_button)
        
        # Down button
        self.down_button = tk.Button(
            self,
            text="↓",
            width=1,
            command=self.down_pressed
        )
        self.down_button.grid(
            row=0,
            column=2,
            sticky=tk.NE
        )
        self.buttons.append(self.down_button)

        # X button
        self.x_button = tk.Button(
            self,
            text="x",
            width=1,
            command=self.master.delete
        )
        self.x_button.grid(
            row=0,
            column=3,
            sticky=tk.NE
        )
        self.buttons.append(self.x_button)

        # Name entry - only shows when renaming the group

        self.name_entry = tk.Entry(
            self,
            width=5
        )
        self.name_entry.bind("<KeyPress>", self.key_pressed)

        # Configure column size for grid layout
        min_size = 720 - (30 * len(self.buttons))
        self.columnconfigure(0, minsize=min_size)

    def refresh_colors(self, colors):

        self.colors = colors

        self.configure(bg=self.colors["BG2"])

        self.name_label.configure(
            bg=self.colors["BG2"],
            fg=self.colors["HL2"]
        )

        for button in self.buttons:
            button.configure(
                highlightbackground=self.colors["BG2"]
            )

        self.name_entry.configure(
            bg=self.colors["BG2"],
            fg=self.colors["HL2"]
        )


    def show_name_entry(self, event):
        self.name_label.grid_remove()
        self.name_entry.grid(
            row=0,
            column=0,
            columnspan=5,
            padx=PADDING,
            pady=PADDING
        )
        self.name_entry.focus_set()
        self.name_entry.delete(0, tk.END)
        self.name_entry.insert(0, self.name)
        self.name_entry.select_range(start=0, end=tk.END)

    def hide_name_entry(self):
        self.name_entry.grid_remove()
        self.name_label.grid()

    def key_pressed(self, event):
        if event.keysym == "Return":
            new_name = self.name_entry.get()
            if len(new_name) > 0:
                self.master.master.master.master.rename_group(self.name, new_name)
                self.master.name = new_name
                self.name = new_name
                self.name_label.configure(text=new_name)
                self.hide_name_entry()
                self.master.master.master.master.master.bottom_frame.input.focus_set()


    def up_pressed(self):
        self.master.master.master.master.move_group(self.name, "up")

    def down_pressed(self):
        self.master.master.master.master.move_group(self.name, "down")