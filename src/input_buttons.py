import tkinter as tk

from constants import *

class InputButtons(tk.Frame):
    def __init__(self, master):

        self.width = 200
        self.height = 100

        tk.Frame.__init__(
            self,
            master,
            width=self.width,
            height=self.height
        )
        self.master = master
        self.buttons = []

        self.create_widgets()

    def create_widgets(self):

        self.submit_button = tk.Button(
            self, 
            text="Submit", 
            command=self.master.submit
        )
        self.submit_button.grid(row=0, column=1)
        self.buttons.append(self.submit_button)

        self.insert_button = tk.Button(
            self,
            text="Insert",
            command=self.master.insert
        )
        self.insert_button.grid(row=1, column=1)
        self.buttons.append(self.insert_button)

        self.save_button = tk.Button(
            self, 
            text="Save", 
            command=self.master.save
        )
        self.save_button.grid(row=2, column=1)
        self.buttons.append(self.save_button)

        self.load_button = tk.Button(
            self,
            text="Load",
            command=self.master.load
        )
        self.load_button.grid(row=3, column=1)
        self.buttons.append(self.load_button)

        self.clear_button = tk.Button(
            self,
            text="Clear",
            command=self.master.clear
        )
        self.clear_button.grid(row=4, column=1)
        self.buttons.append(self.clear_button)

        self.settings_button = tk.Button(
            self,
            text="Settings",
            command=self.master.master.show_settings
        )
        self.settings_button.grid(row=0, column=2)
        self.buttons.append(self.settings_button)

        self.find_button = tk.Button(
            self,
            text="Find",
            command=self.master.show_find_window
        )
        self.find_button.grid(row=1, column=2)
        self.buttons.append(self.find_button)

        self.export_button = tk.Button(
            self,
            text="Export",
            command=self.master.export
        )
        self.export_button.grid(row=2, column=2)
        self.buttons.append(self.export_button)

        self.stats_button = tk.Button(
            self,
            text="Stats",
            command=self.master.show_stats
        )
        self.stats_button.grid(row=3, column=2)
        self.buttons.append(self.stats_button)


        # Configure all buttons

        for button in self.buttons:
            if PLATFORM == "Windows":
                button.configure(width=6)
            else:
                button.configure(width=3)
            button.grid_configure(padx=2, pady=2)

    def refresh_colors(self, colors):
        self.colors = colors

        self.configure(
            bg=self.colors["BG2"]
        )

        for button in self.buttons:
            button.configure(
                highlightbackground=self.colors["BG2"]
            )
            if PLATFORM == "Windows":
                button.configure(
                    bg=self.colors["BG1"],
                    fg=self.colors["HL2"]
                )