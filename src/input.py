import tkinter as tk
import tkinter.font as tkFont

from time import sleep
from sys import exit

from constants import *
from data import *
from key import *
from input_path import *
from save_prompt import *

class Input(tk.Frame):
    def __init__(self, width, height, bg, master=None):
        tk.Frame.__init__(
            self, 
            master, 
            width=width, 
            height=height, 
            bg=bg
        )

        self.inputFont = tkFont.Font(
            self, 
            family=INPUT_FONT_FAMILY, 
            size=INPUT_FONT_SIZE
        )

        self.num_buttons = 4

        self.create_widgets()

        # Key object handles key press and release methods for Text widget
        self.key = Key(self)

        # Key press and release bindings
        self.input.bind('<KeyPress>', self.key.key_press)
        self.input.bind('<KeyRelease>', self.key.key_release)

        # Set up protocol event for window exit
        self.master.master.protocol("WM_DELETE_WINDOW", self.destroy)
        self.saved = False

    def destroy(self, event=None):
        if self.saved == False:
            self.save_prompt = SavePrompt(self)
            self.saved = True

        else:
            exit()

    def submit(self):
        add_entry(self.input.get("1.0", "end"))
        self.master.refresh_entries()
        self.input.delete("1.0", "end")

    def save(self):
        self.input_path = InputPath(self, "save")

    def load(self):
        self.input_path = InputPath(self, "load")

    def save_submit(self, filepath):
        save(filepath)

    def load_submit(self, filepath):
        load(filepath)
        self.master.refresh_entries()

    def clear(self):
        clear()
        self.master.refresh_entries()

    def create_widgets(self):
        self.input = tk.Text(
            self, 
            height=INPUT_HEIGHT, 
            width=INPUT_WIDTH,
            bg=colors["BG1"],
            fg=colors["HL2"],
            font=self.inputFont,
            highlightbackground=colors["BG2"],
            highlightcolor=colors["HL1"]
        )
        self.input.grid(
            row=0, 
            column=0, 
            padx=PADDING, 
            pady=PADDING,
            rowspan=self.num_buttons
        )
        self.input.focus_set()

        self.submit_button = tk.Button(
            self, 
            text="Submit", 
            command=self.submit,
            highlightbackground=colors["BG2"]
        )
        self.submit_button.grid(
            row=0, 
            column=1, 
            padx=PADDING
        )

        self.save_button = tk.Button(
            self, 
            text="Save", 
            command=self.save,
            highlightbackground=colors["BG2"]
        )
        self.save_button.grid(
            row=1, 
            column=1, 
            padx=PADDING
        )

        self.load_button = tk.Button(
            self,
            text="Load",
            command=self.load,
            highlightbackground=colors["BG2"]
        )
        self.load_button.grid(
            row=2, 
            column=1, 
            padx=PADDING
        )

        self.clear_button = tk.Button(
            self,
            text="Clear",
            command=self.clear,
            highlightbackground=colors["BG2"]
        )
        self.clear_button.grid(
            row=3,
            column=1,
            padx=PADDING
        )