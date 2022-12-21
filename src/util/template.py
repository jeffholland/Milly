import tkinter as tk

from constants import *

class ExportWindow(tk.Frame):
    def __init__(self, master):

        self.width = 200
        self.height = 100

        tk.Frame.__init__(
            self,
            master,
            width=self.width,
            height=self.height
        )
        self.master = master

        self.create_widgets()
        self.refresh_colors()

    def create_widgets(self):
        pass

    def refresh_colors(self):
        pass