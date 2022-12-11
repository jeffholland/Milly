import tkinter as tk
import tkinter.font as tkFont

from sys import exit

from constants import *
from colors import get_colors
from data import *
from key import Key
from input_path import InputPath
from insert_prompt import InsertPrompt
from save_prompt import SavePrompt


class Input(tk.Frame):
    def __init__(self, width, height, master=None):
        tk.Frame.__init__(
            self, 
            master, 
            width=width, 
            height=height
        )

        self.inputFont = tkFont.Font(
            self, 
            family=INPUT_FONT_FAMILY, 
            size=INPUT_FONT_SIZE
        )

        # Button array to efficiently configure all buttons
        self.buttons = []
        self.num_buttons = 5

        # Input path set to None by default
        self.input_path = None

        self.create_widgets()

        self.refresh_colors()

        # Key object handles key press and release methods for Text widget
        self.key = Key(self)

        # Key press and release bindings
        self.input.bind('<KeyPress>', self.key.key_press)
        self.input.bind('<KeyRelease>', self.key.key_release)

        # Set up protocol event for window exit
        self.master.master.protocol("WM_DELETE_WINDOW", self.destroy)

        # Bool for exiting after save
        self.exit_after_saving = False

    def destroy(self, event=None):
        if change_detected():
            self.save_prompt = SavePrompt(self)
        else:
            exit()

    def submit(self):
        add_entry(self.input.get("1.0", "end"))
        self.master.refresh_entries()
        self.input.delete("1.0", "end")

    def insert(self):
        if len(get_entries()) == 0:
            self.submit()
        else:
            self.insert_prompt = InsertPrompt(self)

    def save(self, and_exit=False):
        self.input_path = InputPath(self, "save")

        if and_exit:
            self.exit_after_saving = True

    def load(self):
        self.input_path = InputPath(self, "load")

    def save_submit(self, filepath):
        save_entries(filepath)

        if self.exit_after_saving:
            exit()

    def load_submit(self, filepath):
        load_entries(filepath)
        self.master.refresh_entries()

    def clear(self):
        clear_entries()
        self.master.refresh_entries()

    def remove_first_entry(self):
        remove_entry(0)
        self.master.refresh_entries()

    def remove_last_entry(self):
        remove_entry(len(get_entries()) - 1)
        self.master.refresh_entries()

    def create_widgets(self):
        self.input = tk.Text(
            self, 
            height=INPUT_HEIGHT, 
            width=INPUT_WIDTH,
            font=self.inputFont,
            wrap=tk.WORD
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
            command=self.submit
        )
        self.submit_button.grid(
            row=0, 
            column=1, 
            padx=PADDING
        )
        self.buttons.append(self.submit_button)

        self.insert_button = tk.Button(
            self,
            text="Insert",
            command=self.insert
        )
        self.insert_button.grid(
            row=1,
            column=1,
            padx=PADDING
        )
        self.buttons.append(self.insert_button)

        self.save_button = tk.Button(
            self, 
            text="Save", 
            command=self.save
        )
        self.save_button.grid(
            row=2, 
            column=1, 
            padx=PADDING
        )
        self.buttons.append(self.save_button)

        self.load_button = tk.Button(
            self,
            text="Load",
            command=self.load
        )
        self.load_button.grid(
            row=3, 
            column=1, 
            padx=PADDING
        )
        self.buttons.append(self.load_button)

        self.clear_button = tk.Button(
            self,
            text="Clear",
            command=self.clear
        )
        self.clear_button.grid(
            row=4,
            column=1,
            padx=PADDING
        )
        self.buttons.append(self.clear_button)

    def refresh_colors(self):
        self.colors = get_colors()

        self.input.configure(
            bg=self.colors["BG1"],
            fg=self.colors["HL2"],
            highlightbackground=self.colors["BG2"],
            highlightcolor=self.colors["HL1"]
        )

        for button in self.buttons:
            button.configure(
                highlightbackground=self.colors["BG2"]
            )

        if (self.input_path):
            self.input_path.refresh_colors()