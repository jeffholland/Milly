import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

import json
import re

from constants import *
from colors import *

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

        self.create_widgets()

        self.load_settings()

        self.cmd_pressed = False
        self.bind_all("<KeyPress>", self.key_pressed)
        self.bind_all("<KeyRelease>", self.key_released)

    def key_pressed(self, event):
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
        if "Meta" in event.keysym:
            self.cmd_pressed = False

    def create_widgets(self):

        # dcs = default color scheme

        self.dcs_label = tk.Label(
            self,
            text="Default color scheme: "
        )
        self.dcs_label.grid(
            row=0,
            column=0,
            padx=PADDING,
            pady=PADDING
        )
        self.labels.append(self.dcs_label)

        self.dcs_var = tk.StringVar(self)
        self.dcs_selector = ttk.Combobox(
            self,
            textvariable=self.dcs_var,
            values=get_color_schemes(),
            state="readonly"
        )
        self.dcs_selector.grid(
            row=0,
            column=1,
            padx=PADDING,
            pady=PADDING,
            columnspan=3
        )
        self.dcs_var.set("navy")
        self.dcs_selector.bind(
            "<<ComboboxSelected>>", 
            self.default_color_scheme_changed
        )


        # ncs = new color scheme

        self.ncs_label = tk.Label(
            self,
            text="New color scheme:"
        )
        self.ncs_label.grid(
            row=1,
            column=0,
            padx=PADDING,
            pady=PADDING
        )
        self.labels.append(self.ncs_label)

        self.ncs_entries = []
        for i in range(4):
            self.ncs_entries.append(
                tk.Entry(
                    self,
                    width=6
                )
            )
            self.ncs_entries[i].grid(
                row=1,
                column=1+i,
                padx=PADDING,
                pady=PADDING
            )

        self.ncs_name_label = tk.Label(
            self,
            text="Name:"
        )
        self.ncs_name_label.grid(
            row=1, 
            column=5,
            padx=PADDING,
            pady=PADDING
        )
        self.labels.append(self.ncs_name_label)

        self.ncs_name_entry = tk.Entry(
            self,
            width=10
        )
        self.ncs_name_entry.grid(
            row=1, 
            column=6,
            padx=PADDING,
            pady=PADDING
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

        for entry in self.ncs_entries:
            entry.configure(
                bg=self.colors["BG2"],
                fg=self.colors["HL2"]
            )

        self.ncs_name_entry.configure(
            bg=self.colors["HL1"],
            fg=self.colors["BG1"]
        )

    def refresh_settings(self):
        self.dcs_var.set(
            self.settings_data["default_color_scheme"]
        )
        set_color_scheme(self.settings_data["default_color_scheme"])
        self.refresh_colors()

    # Handlers

    def default_color_scheme_changed(self, event):
        self.settings_data["default_color_scheme"] = self.dcs_var.get()

    def save_settings(self):
        # Submit new color scheme if all boxes non-empty
        submit = True
        for entry in self.ncs_entries:
            if len(entry.get()) < 6:
                submit = False
        if submit:
            self.ncs_submit()

        with open("json/settings.json", "w") as f:
            json.dump(self.settings_data, f)

        self.load_settings()

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

    
    # New color scheme functions

    def ncs_submit(self):
        scheme = self.ncs_validate_input()

        if scheme:
            new_color_scheme(scheme, 
                name=self.ncs_name_entry.get())

    def ncs_validate_input(self):
        hexes = []

        for entry in self.ncs_entries:
            hex = entry.get()
            match = None

            # Use Regex to see if all strings are valid hex code
            if len(hex) == 7:
                # print(f"len is 7: {hex}")
                match = re.search(r'^#(?:[0-9a-fA-F]{3}){1,2}$', hex)
            elif len(hex) == 6:
                # print(f"len is 6: {hex}")
                match = re.search(r'^(?:[0-9a-fA-F]{3}){1,2}$', hex)

            if match:
                # Add hash code if not already present
                if (hex[0] != "#"):
                    hex = "#" + hex
                hexes.append(hex)
            else:
                messagebox.showinfo("Hex code invalid", "One or more hex codes invalid. Input rejected")
                return None

        return {
            "BG1": hexes[0],
            "BG2": hexes[1],
            "HL1": hexes[2],
            "HL2": hexes[3]
        }