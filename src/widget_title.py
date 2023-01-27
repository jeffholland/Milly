import tkinter as tk

from constants import *
from data import *
from widget import Widget

class Title(Widget):
    def __init__(self, master, data, index, 
        font):

        Widget.__init__(self, master, data, index)

        self.title = data["title"]
        self.index = index

        self.font = font.copy()
        self.font.configure(size=20)

        self.create_widgets()

    def create_widgets(self):
        # Title text
        self.title_label = tk.Label(
            self,
            text=self.title,
            font=self.font
        )
        self.title_label.grid(
            row=0, 
            column=0, 
            padx=PADDING, 
            pady=PADDING
        )

        # Text entry only shows when title is clicked on
        self.title_label.bind("<Button-1>", self.show_title_entry)

        self.title_var = tk.StringVar()
        self.title_entry = tk.Entry(
            self,
            textvariable=self.title_var
        )
        self.title_entry.bind("<KeyPress>", self.key_pressed)


    def refresh_colors(self, colors):
        self.title_label.configure(
            bg=colors["BG2"],
            fg=colors["HL2"]
        )

        return super().refresh_colors(colors)



    def key_pressed(self, event):
        if event.keysym == "Return":
            new_title = self.title_entry.get()
            self.data["title"] = new_title

            widget_configure(
                self.master.index, 
                self.master.group,
                self.index,
                self.data
            )

            self.title_label.configure(text=new_title)

            self.hide_title_entry()
            self.master.master.master.master.master.bottom_frame.input.focus_set()



    def show_title_entry(self, event):
        self.title_label.grid_remove()
        self.title_entry.grid(
            row=0,
            column=0,
            padx=PADDING,
            pady=PADDING
        )
        self.title_entry.focus_set()
        self.title_entry.delete(0, tk.END)
        self.title_entry.insert(0, self.title)
        self.title_entry.select_range(start=0, end=tk.END)

    def hide_title_entry(self):
        self.title_entry.grid_remove()
        self.title_label.grid()