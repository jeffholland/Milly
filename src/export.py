import tkinter as tk

import csv

from constants import *

class ExportWindow(tk.Frame):
    def __init__(self, master):

        self.width = 280
        self.height = 100

        tk.Frame.__init__(
            self,
            master,
            width=self.width,
            height=self.height
        )
        self.master = master

        self.buttons = []

        self.create_widgets()
        self.refresh_colors()

    def create_widgets(self):
        self.window = tk.Toplevel(self)
        self.window.geometry(f"{self.width}x{self.height}")
        self.window.overrideredirect(True)

        self.csv_button = tk.Button(
            self.window,
            text="csv",
            command=self.export_csv
        )
        self.csv_button.grid(
            row=0,
            column=0,
            padx=PADDING,
            pady=PADDING
        )
        self.buttons.append(self.csv_button)

        self.filename_var = tk.StringVar()
        self.filename_entry = tk.Entry(
            self.window,
            textvariable=self.filename_var
        )
        self.filename_entry.grid(
            row=0, 
            column=1, 
            padx=PADDING, 
            pady=PADDING
        )
        self.filename_entry.focus_set()



    def refresh_colors(self):
        self.colors = self.master.master.colors_obj.get_colors()

        self.window.configure(bg=self.colors["BG2"])

        for button in self.buttons:
            button.configure(highlightbackground=self.colors["BG2"])


    def export_csv(self):
        filename = self.filename_var.get()

        if ".csv" not in filename:
            filename = filename + ".csv"

        with open(filename, "w") as csvfile:
            writer = csv.writer(csvfile)
            for entry in self.master.entries:
                writer.writerow([entry.text])

        self.window.withdraw()