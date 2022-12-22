import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

import re  # for validating hex codes

from constants import *
from show_schemes import ShowColorSchemes


class ColorSchemeSettings(tk.Frame):
    def __init__(self, master):

        tk.Frame.__init__(
            self, 
            master, 
            width=WIDTH - PADDING_BIG * 2, 
            height=120
        )

        self.labels = []
        self.buttons = []

        self.create_widgets()



    def create_widgets(self):
        # title label

        self.title_label = tk.Label(
            self,
            text="Color Scheme",
            justify=tk.CENTER
        )
        self.title_label.grid(
            row=0,
            column=0,
            columnspan=10
        )
        self.labels.append(self.title_label)

        # dcs = default color scheme

        # label
        self.dcs_label = tk.Label(
            self,
            text="Default color scheme: "
        )
        self.dcs_label.grid(
            row=1,
            column=0,
            padx=PADDING,
            pady=PADDING
        )
        self.labels.append(self.dcs_label)

        # selector
        self.dcs_var = tk.StringVar(self)
        self.dcs_selector = ttk.Combobox(
            self,
            textvariable=self.dcs_var,
            values=self.master.master.colors_obj.get_color_schemes(),
            state="readonly",
            takefocus=0
        )
        self.dcs_selector.grid(
            row=1,
            column=1,
            padx=PADDING,
            pady=PADDING,
            columnspan=3
        )
        self.dcs_selector.bind(
            "<<ComboboxSelected>>", 
            self.default_color_scheme_changed
        )

        # left arrow button
        self.dcs_arrow_left = tk.Button(
            self,
            text="<<",
            width=1,
            command=lambda: self.dcs_switch("left")
        )
        self.dcs_arrow_left.grid(
            row=1,
            column=4,
            padx=PADDING,
            pady=PADDING
        )
        self.buttons.append(self.dcs_arrow_left)

        # right arrow button
        self.dcs_arrow_right = tk.Button(
            self,
            text=">>",
            width=1,
            command=lambda: self.dcs_switch("right")
        )
        self.dcs_arrow_right.grid(
            row=1,
            column=5,
            padx=PADDING,
            pady=PADDING
        )
        self.buttons.append(self.dcs_arrow_right)

        
        # show color scheme button
        self.show_color_scheme_button = tk.Button(
            self,
            text="Show all",
            command=self.show_color_schemes
        )
        self.show_color_scheme_button.grid(row=1, column=6)
        self.buttons.append(self.show_color_scheme_button)


        # ncs = new color scheme

        self.ncs_label = tk.Label(
            self,
            text="New color scheme:"
        )
        self.ncs_label.grid(
            row=2,
            column=0,
            padx=PADDING,
            pady=PADDING
        )
        self.labels.append(self.ncs_label)

        # Four entry fields for hex codes
        # BG1, BG2, HL1, and HL2

        self.ncs_entries = []
        for i in range(4):
            self.ncs_entries.append(tk.Entry(self, width=6))
            self.ncs_entries[i].grid(
                row=2,
                column=1+i,
                padx=PADDING,
                pady=PADDING
            )

        # Entry for naming the color scheme

        self.ncs_name_label = tk.Label(
            self,
            text="Name:"
        )
        self.ncs_name_label.grid(
            row=2, 
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
            row=2, 
            column=6,
            padx=PADDING,
            pady=PADDING
        )
        self.ncs_name_entry.bind("<KeyPress>", self.ncs_name_key_pressed)

        self.color_scheme_window = ShowColorSchemes(self)
        self.color_scheme_window.window.withdraw()



    def refresh_colors(self, colors):
        self.colors = colors

        self.configure(
            bg=self.colors["BG2"]
        )

        try:
            self.dcs_var.set(
                self.master.settings_data["default_color_scheme"]
            )
        except KeyError:
            messagebox.showerror("Default color scheme not loaded",
                "Error: Could not find the default color scheme. Ensure that settings have been properly loaded.")
        
        self.dcs_selector["values"] = (
            self.master.master.colors_obj.get_color_schemes()
        )
        self.dcs_selector_style = ttk.Style()
        self.dcs_selector_style.theme_use("alt")
        self.dcs_selector_style.configure(
            "TCombobox",
            fieldbackground=self.colors["BG2"],
            background=self.colors["BG1"],
            foreground=self.colors["BG2"]
        )

        for button in self.buttons:
            button.configure(
                highlightbackground=self.colors["BG2"]
            )

        for entry in self.ncs_entries:
            entry.configure(
                bg=self.colors["HL1"],
                fg=self.colors["BG1"]
            )

        for label in self.labels:
            label.configure(
                bg=self.colors["BG2"],
                fg=self.colors["HL2"]
            )

        self.ncs_name_entry.configure(
            bg=self.colors["HL1"],
            fg=self.colors["BG1"]
        )

    def default_color_scheme_changed(self, event=None):
        self.master.settings_data["default_color_scheme"] = self.dcs_var.get()
        self.master.save_settings()

    def dcs_switch(self, dir):
        vals = self.dcs_selector["values"]
        index = vals.index(self.dcs_var.get())

        if dir == "left":
            if index <= 0:
                new_index = len(vals) - 1
            else:
                new_index = index - 1
        else:
            if index >= len(vals) - 1:
                new_index = 0
            else:
                new_index = index + 1

        self.dcs_var.set(vals[new_index])
        self.default_color_scheme_changed()

    
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

        self.master.settings_data["default_color_scheme"] = self.ncs_name_entry.get()
        self.master.refresh_colors(self.colors)

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
            self.master.save_settings()

    def show_color_schemes(self):
        self.color_scheme_window.window.deiconify()