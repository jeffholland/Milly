import tkinter as tk

from constants import *
from widget import Widget

class Title(Widget):
    def __init__(self, master, title, width, height, font):

        Widget.__init__(
            self, 
            master, 
            width=width, 
            height=height
        )

        self.title = title
        self.type = "Title"

        self.font = font.copy()
        self.font.configure(size=20)

        self.create_widgets()

    def create_widgets(self):
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