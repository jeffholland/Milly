import tkinter as tk

from constants import *

class GroupWindow(tk.Frame):
    def __init__(self, master, group_names):

        self.width = 300
        self.height = 300

        tk.Frame.__init__(
            self,
            master,
            width=self.width,
            height=self.height
        )
        self.master = master

        self.group_names = group_names

        self.labels = []
        self.buttons = []

        self.create_widgets()



    def create_widgets(self):
        self.window = tk.Toplevel(self)
        self.window.geometry(f"{self.width}x{self.height}")

        self.list_var = tk.StringVar()
        self.list_var.set(self.group_names)
        self.group_list = tk.Listbox(
            self.window,
            listvariable=self.list_var
        )
        self.group_list.grid(
            row=0,
            column=0,
            columnspan=5,
            padx=PADDING,
            pady=PADDING
        )

        self.add_button = tk.Button(
            self.window,
            width=1,
            text="+",
            command=self.add_group
        )
        self.add_button.grid(
            row=1,
            column=0
        )



    def add_group(self):
        print("add group")



    def refresh_colors(self, colors):
        self.colors = colors

        for label in self.labels:
            label.configure(
                bg=self.colors["BG1"],
                fg=self.colors["HL2"]
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