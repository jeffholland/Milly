import tkinter as tk

from constants import *

class Template(tk.Frame):
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

        self.labels = []
        self.buttons = []

        self.create_widgets()



    def create_widgets(self):
        self.window = tk.Toplevel(self)
        self.window.geometry(f"{self.width}x{self.height}")
        self.window.title("Template")
        self.window.overrideredirect(True)



    def refresh_colors(self, colors):
        self.colors = colors