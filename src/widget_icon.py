import tkinter as tk

from widget import Widget

class Icon(Widget):
    def __init__(self, master, data, index):
        Widget.__init__(
            self,
            master,
            data,
            index
        )

        self.master = master
        self.data = data
        self.index = index

        self.create_widgets()

    def create_widgets(self):
        self.no_icon_label = tk.Label(
            self,
            text="No icon"
        )

        if self.data["icon"] == None:
            self.no_icon_label.grid(row=0, column=0)
