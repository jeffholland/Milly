import tkinter as tk
from tkinter import messagebox

import json

from constants import *
from settings_colorscheme import ColorSchemeSettings
from settings_entry import EntrySettings
from settings_font import FontSettings



class Settings(tk.Frame):
    def __init__(self, master, width, height):
        tk.Frame.__init__(
            self,
            master,
            width=width,
            height=height
        )

        self.labels = []
        self.buttons = []
        
        self.settings_data = dict()
        self.color_scheme_settings = None

        # Load data from settings.json into self.settings_data
        self.load_settings()

        self.cmd_pressed = False

        self.create_widgets()


    def load_settings(self):
        try:
            f = open(SETTINGS_PATH, "r")
        except OSError:
            messagebox.showerror("Could not open settings.json. Make sure the file exists")

        with f:
            self.settings_data = json.load(f)



    def create_widgets(self):

        # Color scheme settings

        self.color_scheme_settings = ColorSchemeSettings(self)
        self.color_scheme_settings.grid_propagate(0)
        self.color_scheme_settings.grid(
            row=0, 
            column=0,
            padx=PADDING_BIG,
            pady=PADDING_BIG,
            columnspan=3
        )


        # Entry settings

        self.entry_settings = EntrySettings(self)
        self.entry_settings.grid_propagate(0)
        self.entry_settings.grid(
            row=1, 
            column=0,
            padx=PADDING_BIG,
            pady=PADDING_BIG,
            columnspan=3
        )


        # Font settings

        self.font_settings = FontSettings(self)
        self.font_settings.grid_propagate(0)
        self.font_settings.grid(
            row=2, 
            column=0,
            padx=PADDING_BIG,
            pady=PADDING_BIG,
            columnspan=3
        )



        # Main buttons

        self.save_button = tk.Button(
            self,
            text="Save",
            command=self.save_settings
        )
        self.save_button.grid(
            row=10,
            column=0
        )
        self.buttons.append(self.save_button)

        self.load_button = tk.Button(
            self,
            text="Load",
            command=self.load_settings
        )
        self.load_button.grid(
            row=10,
            column=1
        )
        self.buttons.append(self.load_button)

        self.back_button = tk.Button(
            self,
            text="Back",
            command=self.back
        )
        self.back_button.grid(
            row=10,
            column=2
        )
        self.buttons.append(self.back_button)



    def refresh_colors(self, colors):
        self.colors = colors

        self.color_scheme_settings.refresh_colors(colors)
        self.entry_settings.refresh_colors(colors)
        self.font_settings.refresh_colors(colors)

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
            if PLATFORM == "Windows":
                button.configure(
                    bg=self.colors["BG2"],
                    fg=self.colors["HL2"]
                )
        


    def apply_settings(self):

        # Color scheme settings

        self.master.colors_obj.set_color_scheme(self.settings_data["default_color_scheme"])

        # Entry settings

        self.entry_settings.show_checkboxes_var.set(self.settings_data["show_checkboxes"])
        self.entry_settings.show_checkboxes_pressed()

        self.entry_settings.show_dates_var.set(self.settings_data["show_dates"])
        self.entry_settings.show_dates_pressed()

        self.entry_settings.show_times_var.set(self.settings_data["show_times"])
        self.entry_settings.show_times_pressed()

        self.entry_settings.show_menu_var.set(self.settings_data["show_menu"])
        self.entry_settings.show_menu_pressed()

        # Font settings

        self.font_settings.font_family_var.set(self.settings_data["font_family"])
        self.font_settings.apply_pressed()

        self.master.refresh_colors()



    def save_settings(self):

        # Check for new color scheme data entered
        # save it if detected.
        self.color_scheme_settings.ncs_check()
        
        with open(SETTINGS_PATH, "w") as f:
            json.dump(self.settings_data, f)

        self.load_settings()
        self.apply_settings()



    def key_pressed(self, event):
        if PLATFORM == "Windows":
            if "Control" in event.keysym:
                self.cmd_pressed = True
        else:
            if "Meta" in event.keysym:
                self.cmd_pressed = True

        if event.keysym == "Escape":
            self.back()

        if self.cmd_pressed:
            if event.keysym.lower() == "s":
                self.save_settings()
            if event.keysym.lower() == "l":
                self.load_settings()
                self.apply_settings()

    def key_released(self, event):
        if PLATFORM == "Windows":
            if "Control" in event.keysym:
                self.cmd_pressed = False
        else:
            if "Meta" in event.keysym:
                self.cmd_pressed = False



    def back(self):
        self.master.hide_settings()