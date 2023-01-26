import tkinter as tk

from constants import *

class Widget(tk.Frame):
    def __init__(self, master, width, height):

        tk.Frame.__init__(
            self, 
            master, 
            width=width, 
            height=height
        )

        self.master = master
        self.width = width
        self.height = height

        self.create_widgets()

    def create_widgets(self):
        self.title_label = tk.Label(
            self,
            text="Widget"
        )
        self.title_label.grid(
            row=0, 
            column=0, 
            padx=PADDING, 
            pady=PADDING
        )

    def refresh_colors(self, colors):
        self.colors = colors
        
        self.configure(bg=colors["BG2"])

        self.title_label.configure(
            bg=colors["BG2"],
            fg=colors["HL2"]
        )