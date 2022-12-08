import tkinter as tk

from os import path

from constants import *

class InputPath(tk.Frame):
    def __init__(self, master):
        self.master = master

        self.window = tk.Toplevel(master)

        self.window.title("Input filepath")

        self.window.geometry("200x50")

        self.create_widgets()

        # self.master.load_submit(FILEPATH)

    def key_press(self, event):
        if (event.keysym == "Return"):
            input_string = self.entry.get()

            if input_string[:5] != "json/":
                input_string = "json/" + input_string

            if input_string[-5:] != ".json":
                input_string = input_string + ".json"

            if (path.isfile(input_string)):
                self.master.load_submit(input_string)
            else:
                print("Could not open file: " + input_string)

    def create_widgets(self):
        self.entry = tk.Entry(self.window)
        self.entry.grid(row=0, column=0)

        self.entry.bind('<KeyPress>', self.key_press)