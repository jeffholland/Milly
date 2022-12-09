import tkinter as tk

from os import path

from constants import *
from data import get_last_filepath

class InputPath(tk.Frame):
    def __init__(self, master, mode):
        self.master = master

        # Mode = "save" or "load"
        self.mode = mode

        self.window = tk.Toplevel(master)
        self.window.title("Input filepath")
        self.window.geometry("200x50")

        self.create_widgets()
    

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
                    print("Could not load file: " + input_string)
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