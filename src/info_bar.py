import tkinter as tk

from colors import get_current_color_scheme
from constants import *

# Tool for debugging and general info viewing.
# 
# To turn it on: 
# In main.py, set self.show_info_bar to True.

class InfoBar(tk.Frame):
    def __init__(self, master):

        self.master = master
        self.height = 40

        tk.Frame.__init__(
            self,
            master,
            width=WIDTH,
            height=self.height,
            bg="lightgray"
        )

        self.create_widgets()



    def create_widgets(self):

        self.cs_var = tk.StringVar(self)
        self.cs_label = tk.Label(
            self,
            textvariable=self.cs_var,
            bg="lightgray",
            fg="black"
        )
        self.cs_label.grid(row=0, column=0)
        self.set_color_scheme()



    def set_color_scheme(self):
        self.cs_var.set(get_current_color_scheme())