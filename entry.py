import tkinter as tk
import tkinter.font as tkFont

from constants import *

class Entry(tk.Frame):
    def __init__(self, date, text, width, height, bg, master=None):
        tk.Frame.__init__(self, master, width=width, height=height, bg=bg)
        self.date = date
        self.text = text
        self.font = tkFont.Font(family='Helvetica', size=14)

        self.create_widgets()


    def create_widgets(self):
        self.date_label = tk.Label(self, 
            text=str(self.date),
            font=self.font)
        self.date_label.grid(row=0, column=0, sticky=tk.W)

        self.text_label = tk.Label(self, 
            text=self.text,
            bg="white", 
            fg="black", 
            font=self.font)
        self.text_label.grid(row=1, column=0)