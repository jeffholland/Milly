import tkinter as tk
import tkinter.font as tkFont

from sys import exit

from constants import *
from data import *
from find import FindWindow
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

        # Input (Text widget) details

        self.input_height = 7

        if MODE == "fullscreen":
            self.input_width = 130
        else:
            if PLATFORM == "Windows":
                self.input_width = 48
            else:
                self.input_width = 60

        self.input_font = tkFont.Font(
            self, 
            family=INPUT_FONT_FAMILY, 
            size=INPUT_FONT_SIZE
        )

        # Button array to efficiently configure all buttons
        self.buttons = []
        self.num_buttons = 5

        # Input path set to None by default
        # (warning: always set it back to None after closing it)
        
        self.input_path = None

        self.create_widgets()

        self.refresh_colors()

        # object handles key press and release methods for Text widget
        self.key = Key(self)

        # Key press and release bindings
        self.input.bind('<KeyPress>', self.key.key_press)
        self.input.bind('<KeyRelease>', self.key.key_release)

        # Set up protocol event for window exit
        self.master.master.protocol("WM_DELETE_WINDOW", self.destroy)

        # Bool for exiting after save
        self.exit_after_saving = False



    def create_widgets(self):
        self.input = tk.Text(
            self, 
            height=self.input_height, 
            width=self.input_width,
            font=self.input_font,
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

        self.settings_button = tk.Button(
            self,
            text="Settings",
            command=self.master.show_settings
        )
        self.settings_button.grid(
            row=0,
            column=2,
            padx=PADDING
        )
        self.buttons.append(self.settings_button)

        for button in self.buttons:
            if PLATFORM == "Windows":
                button.configure(
                    width=6
                )
            else:
                button.configure(
                    width=3
                )
        
        self.find_window = FindWindow(self)
        self.find_window.window.withdraw()
        # self.input.focus_set()

    def refresh_colors(self):
        self.colors = self.master.colors_obj.get_colors()

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
            if PLATFORM == "Windows":
                button.configure(
                    bg=self.colors["BG1"],
                    fg=self.colors["HL2"]
                )

        if (self.input_path):
            self.input_path.refresh_colors()

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

    def show_find_window(self):
        self.find_window.window.deiconify()
        self.find_window.entry.focus_set()