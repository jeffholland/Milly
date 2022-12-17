import tkinter as tk

import json

from constants import *
from settings_colorscheme import ColorSchemeSettings

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
        
        self.settings_data = None

        self.load_settings()

        self.create_widgets()

        self.cmd_pressed = False
        self.bind_all("<KeyPress>", self.key_pressed)
        self.bind_all("<KeyRelease>", self.key_released)

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

    def key_released(self, event):
        if PLATFORM == "Windows":
            if "Control" in event.keysym:
                self.cmd_pressed = False
        else:
            if "Meta" in event.keysym:
                self.cmd_pressed = False

    def create_widgets(self):

        # Color scheme settings

        self.color_scheme_settings = ColorSchemeSettings(self)
        self.color_scheme_settings.grid_propagate(0)
        self.color_scheme_settings.grid(row=0, column=0)

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

    def refresh_colors(self):
        self.colors = self.master.colors_obj.get_colors()
        
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

    def refresh_settings(self):           
        self.refresh_colors()

    # Handlers

    def save_settings(self):
        with open("json/settings.json", "w") as f:
            json.dump(self.settings_data, f)

        self.load_settings()

        # Check for new color scheme data entered
        # save it if detected.
        self.color_scheme_settings.ncs_check()

    def load_settings(self):
        try:
            f = open("json/settings.json", "r")
        except OSError:
            print("Could not open settings.json. Make sure the file exists")

        with f:
            self.settings_data = json.load(f)
            self.refresh_settings()

    def back(self):
        self.master.hide_settings()