import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

import re

from constants import *

class ColorSchemeSettings(tk.Frame):
    def __init__(self, master):

        tk.Frame.__init__(self, master, width=600, height=400)

        self.labels = []

        self.create_widgets()
        self.refresh_colors()

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
            values=self.master.master.colors_obj.get_color_schemes(),
            state="readonly"
        )
        self.dcs_selector.grid(
            row=0,
            column=1,
            padx=PADDING,
            pady=PADDING,
            columnspan=3
        )
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
        self.ncs_name_entry.bind("<KeyPress>", self.ncs_name_key_pressed)

    def refresh_colors(self):
        self.colors = self.master.master.colors_obj.get_colors()

        self.dcs_var.set(
            self.master.settings_data["default_color_scheme"]
        )
        self.dcs_selector["values"] = (
            self.master.master.colors_obj.get_color_schemes())

        self.master.master.colors_obj.set_color_scheme(
            self.master.settings_data["default_color_scheme"])

        for entry in self.ncs_entries:
            entry.configure(
                bg=self.colors["BG2"],
                fg=self.colors["HL2"]
            )

        for label in self.labels:
            label.configure(
                bg=self.colors["BG1"],
                fg=self.colors["HL2"]
            )

        self.ncs_name_entry.configure(
            bg=self.colors["HL1"],
            fg=self.colors["BG1"]
        )

    def default_color_scheme_changed(self, event):
        self.settings_data["default_color_scheme"] = self.dcs_var.get()

    
    # New color scheme functions

    def ncs_check(self):
        # Submit new color scheme if all boxes non-empty
        submit = True
        for entry in self.ncs_entries:
            if len(entry.get()) < 6:
                submit = False
        if submit:
            self.ncs_submit()

    def ncs_submit(self):
        scheme = self.ncs_validate_input()

        if scheme:
            self.master.master.colors_obj.new_color_scheme(
                scheme, 
                name=self.ncs_name_entry.get()
            )

        self.settings_data["default_color_scheme"] = self.ncs_name_entry.get()
        self.refresh_settings()

        for entry in self.ncs_entries:
            entry.delete(0, tk.END)
        self.ncs_name_entry.delete(0, tk.END)

    def ncs_validate_input(self):
        hexes = []

        for entry in self.ncs_entries:
            hex = entry.get()
            match = None

            # If len is 6, prepend hash.
            if len(hex) == 6:
                hex = "#" + hex

            # If len is 7, use regex to see if it is a valid hex code.
            if len(hex) == 7:
                match = re.search(r'^#(?:[0-9a-fA-F]{3}){1,2}$', hex)

            if match:
                hexes.append(hex)
                continue
            else:
                messagebox.showinfo("Hex code invalid", 
                    "One or more hex codes invalid. Input rejected")
                return None

        return {
            "BG1": hexes[0],
            "BG2": hexes[1],
            "HL1": hexes[2],
            "HL2": hexes[3]
        }

    def ncs_name_key_pressed(self, event):
        if event.keysym == "Return":
            self.save_settings()