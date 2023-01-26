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

    def refresh_colors(self, colors):
        self.colors = colors
        
        self.configure(bg=colors["BG2"])

        self.title_label.configure(
            bg=colors["BG2"],
            fg=colors["HL2"]
        )