import tkinter as tk
import tkinter.font as tkFont

from sys import exit

from constants import *
from data import *
from find import FindWindow
from key import Key
from input_buttons import InputButtons
from input_path import InputPath
from insert_prompt import InsertPrompt
from save_prompt import SavePrompt
from stats import Stats



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

        # Number of buttons high the InputButtons frame is
        self.num_buttons = 5

        # Input path set to None by default
        
        self.input_path = None
        self.save_prompt = None

        # object handles key press and release methods for Text widget
        self.key = Key(self)

        # Set up protocol event for window exit
        self.master.master.protocol("WM_DELETE_WINDOW", self.destroy)

        # Bool for exiting after save
        self.exit_after_saving = False

        self.create_widgets()



    def create_widgets(self):

        # Text input widget

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
        self.input.bind('<KeyPress>', self.key.key_press)
        self.input.bind('<KeyRelease>', self.key.key_release)

        self.input_buttons = InputButtons(self)
        self.input_buttons.grid(row=0, column=1)
        
        self.find = FindWindow(self)
        self.find.window.withdraw()

        self.stats = Stats(self)
        self.stats.window.withdraw()



    def refresh_colors(self, colors):
        self.colors = colors

        self.input.configure(
            bg=self.colors["BG1"],
            fg=self.colors["HL2"],
            highlightbackground=self.colors["BG2"],
            highlightcolor=self.colors["HL1"]
        )

        self.input_buttons.refresh_colors(colors)

        if self.input_path:
            self.input_path.refresh_colors(colors)

        if self.save_prompt:
            self.save_prompt.refresh_colors(colors)

        self.find.refresh_colors(colors)

        self.stats.refresh_colors(colors)



    # Button and key shortcut handlers

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
        self.find.show()

    def export(self):
        self.master.top_frame.export()

    def show_stats(self):
        self.stats.window.deiconify()