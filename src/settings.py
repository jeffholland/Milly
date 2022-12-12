import tkinter as tk
from tkinter import ttk

import json

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

        self.bind_all("<KeyPress>", self.key_pressed)

    def key_pressed(self, event):
        if event.keysym == "Escape":
            self.back()

    def create_widgets(self):
        self.default_color_scheme_label = tk.Label(
            self,
            text="Default color scheme: "
        )
        self.default_color_scheme_label.grid(
            row=0,
            column=0,
            padx=PADDING,
            pady=PADDING
        )
        self.labels.append(self.default_color_scheme_label)

        self.default_color_scheme_var = tk.StringVar(self)
        self.default_color_scheme_selector = ttk.Combobox(
            self,
            textvariable=self.default_color_scheme_var,
            values=get_color_schemes(),
            state="readonly"
        )
        self.default_color_scheme_selector.grid(
            row=0,
            column=1,
            padx=PADDING,
            pady=PADDING
        )
        self.default_color_scheme_var.set("navy")
        self.default_color_scheme_selector.bind(
            "<<ComboboxSelected>>", 
            self.default_color_scheme_changed
        )

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
            bg=self.colors["BG2"]
        )

        for label in self.labels:
            label.configure(
                bg=self.colors["BG2"],
                fg=self.colors["HL2"]
            )

        for button in self.buttons:
            button.configure(
                highlightbackground=self.colors["BG2"]
            )

    def refresh_settings(self):
        self.default_color_scheme_var.set(
            self.settings_data["default_color_scheme"]
        )
        set_color_scheme(self.settings_data["default_color_scheme"])
        self.refresh_colors()

    # Handlers

    def default_color_scheme_changed(self, event):
        self.settings_data["default_color_scheme"] = self.default_color_scheme_var.get()

    def save_settings(self):
        with open("json/settings.json", "w") as f:
            json.dump(self.settings_data, f)

    def load_settings(self):
        try:
            f = open("json/settings.json", "r")
        except OSError:
            print("Could not open settings.json. Make sure the file exists")

        with f:
            self.settings_data = json.load(f)
            self.refresh_settings()

    def back(self):
        # self.unbind_all("<KeyPress>")
        self.master.hide_settings()