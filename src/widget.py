import tkinter as tk

from constants import *

class Widget(tk.Frame):
    def __init__(self, master, data, index):

        self.data = data
        self.index = index
        self.width = data["width"]
        self.height = data["height"]

        tk.Frame.__init__(
            self, 
            master, 
            width=self.width, 
            height=self.height
        )

        self.master = master

    def refresh_colors(self, colors):
        self.colors = colors
        
        self.configure(bg=colors["BG2"])