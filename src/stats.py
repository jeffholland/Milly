import tkinter as tk

from constants import *
from data import *

class Stats(tk.Frame):
    def __init__(self, master):

        self.width = 180
        self.height = 240

        tk.Frame.__init__(
            self,
            master,
            width=self.width,
            height=self.height
        )
        self.master = master

        self.labels = []
        self.buttons = []

        self.create_widgets()



    def create_widgets(self):
        self.window = tk.Toplevel(self)
        self.window.geometry(f"{self.width}x{self.height}")
        self.window.title("Stats")
        self.window.overrideredirect(True)


        # Number of entries

        self.label1 = tk.Label(
            self.window,
            text="Entries: "
        )
        self.label1.grid(row=0, column=0)
        self.labels.append(self.label1)

        self.num_entries_var = tk.StringVar()
        self.num_entries_var.set(0)

        self.num_entries_label = tk.Label(
            self.window,
            textvariable=self.num_entries_var
        )
        self.num_entries_label.grid(row=0, column=1)
        self.labels.append(self.num_entries_label)


        # Number of words

        self.label2 = tk.Label(
            self.window,
            text="Words: "
        )
        self.label2.grid(row=1, column=0)
        self.labels.append(self.label2)

        self.num_words_var = tk.StringVar()
        self.num_words_var.set(0)

        self.num_words_label = tk.Label(
            self.window,
            textvariable=self.num_words_var
        )
        self.num_words_label.grid(row=1, column=1)
        self.labels.append(self.num_words_label)


        # Number of characters

        self.label3 = tk.Label(
            self.window,
            text="Characters: "
        )
        self.label3.grid(row=2, column=0)
        self.labels.append(self.label3)

        self.num_chars_var = tk.StringVar()
        self.num_chars_var.set(0)

        self.num_chars_label = tk.Label(
            self.window,
            textvariable=self.num_chars_var
        )
        self.num_chars_label.grid(row=2, column=1)
        self.labels.append(self.num_chars_label)


        # Number of color schemes

        self.label4 = tk.Label(
            self.window,
            text="Color schemes: "
        )
        self.label4.grid(row=3, column=0)
        self.labels.append(self.label4)

        self.num_schemes_var = tk.StringVar()
        self.num_schemes_var.set(0)

        self.num_schemes_label = tk.Label(
            self.window,
            textvariable=self.num_schemes_var
        )
        self.num_schemes_label.grid(row=3, column=1)
        self.labels.append(self.num_schemes_label)

        
        # OK button

        self.ok_button = tk.Button(
            self.window,
            text="OK",
            command=self.ok_pressed
        )
        self.ok_button.grid(row=10, column=0, columnspan=2)
        self.buttons.append(self.ok_button)


        # Grid configure padding

        for label in self.labels:
            label.grid_configure(padx=PADDING, pady=PADDING)
        for button in self.buttons:
            button.grid_configure(padx=PADDING, pady=PADDING)



    def refresh_colors(self, colors):
        # Set num_schemes here
        self.num_schemes_var.set(
            len(self.master.master.colors_obj.get_color_schemes()))

        self.colors = colors

        self.window.configure(
            bg=self.colors["BG2"]
        )

        for label in self.labels:
            label.configure(
                bg=self.colors["BG2"],
                fg=self.colors["HL2"],
            )

        for button in self.buttons:
            button.configure(
                highlightbackground=self.colors["BG2"]
            )

    def refresh_stats(self):
        entries = get_entries()

        self.num_entries_var.set(len(entries))
        self.num_words_var.set(self.word_count(entries))
        self.num_chars_var.set(self.char_count(entries))



    def word_count(self, entries):
        count = 0

        for entry in entries:
            count += len(entry["text"].split())

        return count

    

    def char_count(self,entries):
        count = 0

        for entry in entries:
            count += len(entry["text"])

        return count

    

    def ok_pressed(self):
        self.window.withdraw()