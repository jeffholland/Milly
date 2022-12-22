import tkinter as tk

class InputButtons(tk.Frame):
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

    def create_widgets(self):
        pass

    def refresh_colors(self, colors):
        self.colors = colors