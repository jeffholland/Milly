import tkinter as tk
from tkinter import messagebox

from os import path, listdir

from constants import *
from data import get_last_filepath

class InputPath(tk.Frame):
    def __init__(self, master, mode):
        self.master = master

        # Mode = "save" or "load"
        self.mode = mode

        # Dimensions
        self.width = 240
        self.height = 80

        self.buttons = []

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
            row=2,
            column=0
        )
        self.buttons.append(self.cancel_button)

        self.ok_button = tk.Button(
            self.window,
            text="Ok",
            command=self.submit
        )
        self.ok_button.grid(
            row=2,
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

            self.browse_button = tk.Button(
                self.window,
                width=3,
                text="Browse",
                command=self.show_browser
            )
            self.browse_button.grid(
                row=0,
                column=2
            )
            self.buttons.append(self.browse_button)

            # File browser - only shows when Browse button is pressed
            self.browser_var = tk.StringVar()
            self.browser = tk.Listbox(
                self.window,
                listvariable=self.browser_var
            )
            self.browser.bind("<<ListboxSelect>>", self.browser_callback)
            self.browser.bind("<Double-1>", self.browser_doubleclick)


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
        if (event.keysym == "Return"):
            self.submit()

    def key_release(self, event):
        # Release command key while in other window
        if PLATFORM == "Windows":
            if "Control" in event.keysym:
                self.master.key.keys_pressed["cmd"] = False
        else:
            if "Meta" in event.keysym:
                self.master.key.keys_pressed["cmd"] = False
                

    def submit(self):
        input_string = self.entry.get()

        if SAVE_DATA_PATH not in input_string:
            input_string = SAVE_DATA_PATH + input_string

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


    # Utility for getting a list of files in a path,
    # formatted to my liking
    def list_files(self, path):
        # Filter .json files
        files = []
        for file in listdir(path):
            # json file - remove .json extension
            if file[-5:] == ".json":
                files.append(file[:-5])
            # directory - add a > symbol
            else:
                files.append(file + "/")
        return files


    def show_browser(self):
        self.browser_var.set(self.list_files(SAVE_DATA_PATH))

        self.browser.grid(
            row=1,
            column=0,
            columnspan=2,
            padx=PADDING,
            pady=PADDING
        )

        self.window.geometry("280x300")


    # Single click to select a json file
    def browser_callback(self, event):
        w = event.widget
        try:
            index = int(w.curselection()[0])
            value = w.get(index)
            # If not a directory (therefore a json file)
            if value[-1] != "/":
                self.entry_var.set(value)
        except IndexError:
            # no selection, nothing to do
            return

    # Double click to select file or enter directory
    def browser_doubleclick(self, event):
        w = event.widget
        try:
            index = int(w.curselection()[0])
            value = w.get(index)
            # Select directory
            if value[-1] == "/":
                # List files in this directory (back button at the top)
                values = self.list_files(SAVE_DATA_PATH + value)
                values.insert(0, "(back)")
                self.browser_var.set(values)
            # Select back button
            if value == "(back)":
                self.browser_var.set(self.list_files(SAVE_DATA_PATH))
            # Select file (not directory or back button)
            if value[-1] != "/" and value != "(back)":
                # File already selected in entry box, so we can just submit
                self.submit()
        except IndexError:
            # no selection, nothing to do
            return