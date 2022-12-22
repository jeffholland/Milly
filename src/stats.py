import tkinter as tk

from constants import *

class Stats(tk.Frame):
    def __init__(self, master):

        self.width = 200
        self.height = 400

        tk.Frame.__init__(
            self,
            master,
            width=self.width,
            height=self.height
        )
        self.master = master

        self.labels = []

        self.create_widgets()

    def create_widgets(self):
        self.window = tk.Toplevel(self)
        self.window.geometry(f"{self.width}x{self.height}")
        self.window.title("Stats")

        # Number of entries

        self.label1 = tk.Label(
            self.window,
            text="Number of entries: "
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

        for label in self.labels:
            label.grid_configure(padx=PADDING, pady=PADDING)

    def refresh_colors(self, colors):
        self.colors = colors

        self.window.configure(
            bg=self.colors["BG2"]
        )

        for label in self.labels:
            label.configure(
                bg=self.colors["BG2"],
                fg=self.colors["HL2"],
            )