import tkinter as tk
from tkinter import messagebox

from os import path

from constants import *
from data import get_last_filepath
from input_path_browser import InputPathBrowser

class InputPath(tk.Frame):
    def __init__(self, master, mode):
        self.master = master

        # Mode = "save" or "load"
        self.mode = mode

        # Dimensions
        self.width = 240
        self.height = 80

        self.buttons = []

        self.load_path = SAVE_DATA_PATH
        
        self.cmd_key_pressed = False

        self.create_widgets()



    def create_widgets(self):
        self.window = tk.Toplevel(self.master)
        self.window.geometry(f"{self.width}x{self.height}")
        self.window.overrideredirect(True)

        self.entry_var = tk.StringVar(self.master)

        self.entry = tk.Entry(
            self.window,
            takefocus=1,
            textvariable=self.entry_var,
            width=14
        )
        self.entry.grid(
            row=0, 
            column=0,
            columnspan=2,
            padx=PADDING,
            pady=PADDING
        )

        self.entry_var.set(get_last_filepath(short=True))

        self.entry.bind('<KeyPress>', self.key_press)
        self.entry.bind('<KeyRelease>', self.key_release)

        self.entry.focus_set()
        self.entry.select_range(start=0, end=tk.END)

        self.cancel_button = tk.Button(
            self.window,
            text="Cancel",
            command=self.cancel
        )
        self.cancel_button.grid(
            row=6,
            column=0
        )
        self.buttons.append(self.cancel_button)

        self.ok_button = tk.Button(
            self.window,
            text="Ok",
            command=self.submit
        )
        self.ok_button.grid(
            row=6,
            column=1
        )
        self.buttons.append(self.ok_button)

        if PLATFORM == "Windows":
            self.ok_button.configure(width=2)
            self.cancel_button.configure(width=5)
        else:
            self.ok_button.configure(width=1)
            self.cancel_button.configure(width=2)


        if self.mode == "load":
            self.browser = InputPathBrowser(self)

        self.browse_button = tk.Button(
            self.window,
            width=3,
            text="Browse",
            command=self.browser.show_browser
        )
        self.browse_button.grid(
            row=0,
            column=2
        )
        self.buttons.append(self.browse_button)


    def refresh_colors(self, colors):
        self.colors = colors

        self.window.configure(
            bg=self.colors["BG1"]
        )

        self.entry.configure(
            bg=self.colors["BG2"],
            fg=self.colors["HL2"],
            highlightbackground=self.colors["HL1"],
            highlightcolor=self.colors["HL2"]
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
    

    def key_press(self, event):
        if event.keysym == "Return":
            self.submit()

        if PLATFORM == "Windows":
            if "Control" in event.keysym:
                self.cmd_key_pressed = True
        else:
            if "Meta" in event.keysym:
                self.cmd_key_pressed = True

        if self.cmd_key_pressed:
            if event.keysym.lower() == "b":
                self.browser.show_browser()
                

    def key_release(self, event):
        # Release command key while in other window
        if PLATFORM == "Windows":
            if "Control" in event.keysym:
                self.master.key.keys_pressed["cmd"] = False
                self.cmd_key_pressed = False
        else:
            if "Meta" in event.keysym:
                self.master.key.keys_pressed["cmd"] = False
                self.cmd_key_pressed = False
                

    def submit(self):
        input_string = self.entry.get()

        if self.load_path not in input_string:
            input_string = self.load_path + input_string

        if input_string[-5:] != ".json":
            input_string = input_string + ".json"

        if self.mode == "load":
            if (path.isfile(input_string)):
                self.master.load_submit(input_string)
            else:
                messagebox.showinfo("Path is not a file", "Could not load filepath: " + input_string)
        if self.mode == "save":
            self.master.save_submit(input_string)

        self.cancel()

    def cancel(self):
        self.window.withdraw()
        self.window.update()
        self.master.winfo_toplevel().deiconify()
        self.master.input.focus_set()

    
    # Utility for getting the window back to normal size
    def reset_window(self):
        self.window.geometry(f"{self.width}x{self.height}")

    def test(self):
        print("hello...")