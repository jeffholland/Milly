import json
from os import scandir

from tkinter import messagebox

from constants import *


class Colors:
    def __init__(self, master):
        self.master = master

        self.color_scheme_index = 0

        self.color_schemes = []

        self.colors = []

        self.load_colors()

    def load_colors(self, refresh=True):
        if refresh:
            self.color_schemes.clear()

            with scandir(COLOR_SCHEME_PATH) as entries:
                for entry in entries:
                    if entry.name[-5:] == ".json":
                        self.color_schemes.append(entry.name[:-5])
            
            self.color_schemes.sort()

            scheme_name = ""

            try:
                with open(SETTINGS_PATH) as f:
                    settings = json.load(f)
                    scheme_name = settings["default_color_scheme"]
            except OSError:
                messagebox.showerror("Settings not found",
                    "Error: settings.json not found. Please make sure it is saved to the correct path.")

        else:
            scheme_name = self.color_schemes[self.color_scheme_index]

        filepath = f"{COLOR_SCHEME_PATH}{scheme_name}.json"

        try:
            with open(filepath, 'r') as f:
                self.colors = json.load(f)
        except OSError:
            messagebox.showerror("Default color scheme not found",
                f"Error: Default color scheme {filepath} not found. \nPlease make sure the default color scheme in settings.json is set to an existing color scheme")


    def get_colors(self):
        return self.colors


    def get_color_schemes(self):
        self.load_colors()
        return self.color_schemes


    def get_color_scheme(self, scheme_name):
        try:
            with open(f"{COLOR_SCHEME_PATH}{scheme_name}.json") as f:
                return json.load(f)
        except OSError:
            messagebox.showerror("Bad color scheme name",
                f"Error: Could not find color scheme \"{scheme_name}\"")


    def get_current_color_scheme(self):
        return self.color_schemes[self.color_scheme_index]


    def switch_color_scheme(self, dir="right"):

        if (dir == "left"):
            if self.color_scheme_index <= 0:
                self.color_scheme_index = len(self.color_schemes) - 1
            else:
                self.color_scheme_index -= 1
        else:
            if self.color_scheme_index >= len(self.color_schemes) - 1:
                self.color_scheme_index = 0
            else:
                self.color_scheme_index += 1
        
        self.load_colors(refresh=False)

    def set_color_scheme(self, name):

        index = self.color_schemes.index(name)
        
        if index >= 0 and index < len(self.color_schemes):
            self.color_scheme_index = index

            self.load_colors()

    def new_color_scheme(self, scheme, name="new_scheme"):
        filepath = f"{COLOR_SCHEME_PATH}{name}.json"

        with open(filepath, "w") as f:
            json.dump(scheme, f)



# utility functions


def hex_to_rgb(hex):

    # stolen from stackoverflow
    hex = hex.lstrip("#")
    lh = len(hex)
    return tuple(int(hex[i:i + lh // 3], 16) for i in range(0, lh, lh // 3))