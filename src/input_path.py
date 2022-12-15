import tkinter as tk
from tkinter import messagebox

from os import path

from colors import get_colors
from constants import *
from data import get_last_filepath

class InputPath(tk.Frame):
    def __init__(self, master, mode):
        self.master = master

        # Mode = "save" or "load"
        self.mode = mode

        # Dimensions
        self.width = 200
        self.height = 50

        self.window = tk.Toplevel(master)
        self.window.title("Input filepath")
        self.window.geometry(f"{self.width}x{self.height}")

        self.create_widgets()

        self.refresh_colors()
    

    def key_press(self, event):
        if (event.keysym == "Return"):
            input_string = self.entry.get()

            if input_string[:5] != "json/":
                input_string = "json/" + input_string

            if input_string[-5:] != ".json":
                input_string = input_string + ".json"

            if self.mode == "load":
                if (path.isfile(input_string)):
                    self.master.load_submit(input_string)
                else:
                    messagebox.showinfo("Path is not a file", "Could not load filepath: " + input_string)
            if self.mode == "save":
                self.master.save_submit(input_string)

            self.window.destroy()
            self.window.update()


    def key_release(self, event):
        # Release command key while in other window
        if event.keysym == "Meta_L" or event.keysym == "Meta_R":
            self.master.key.keys_pressed["cmd"] = False


    def create_widgets(self):
        self.entry_var = tk.StringVar(self.master)

        self.entry = tk.Entry(
            self.window,
            takefocus=1,
            textvariable=self.entry_var
        )

        self.entry_var.set(get_last_filepath(short=True))

        self.entry.grid(row=0, column=0)

        self.entry.bind('<KeyPress>', self.key_press)
        self.entry.bind('<KeyRelease>', self.key_release)

        self.entry.focus_set()
        self.entry.select_range(start=0, end=tk.END)

    def refresh_colors(self):
        self.colors = get_colors()

        try:
            self.window.configure(
                bg=self.colors["BG1"]
            )
        except tk.TclError:
            if DEBUG:
                messagebox.showinfo("TclError", "Known Bug: Attempt to configure window before destroying it.")
            return

        self.entry.configure(
            bg=self.colors["BG2"],
            fg=self.colors["HL2"],
            highlightbackground=self.colors["HL1"],
            highlightcolor=self.colors["HL2"]
        )