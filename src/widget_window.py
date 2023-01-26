import tkinter as tk

from constants import *

class WidgetWindow(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        self.master = master

        # Types of widgets
        self.widget_types = [
            "Title",
            "Icon",
            "Number",
            "Due"
        ]

        self.buttons = []

        self.create_widgets()

    def create_widgets(self):
        self.window = tk.Toplevel(self.master)

        count = 0
        for type in self.widget_types:
            self.buttons.append(tk.Button(
                self.window,
                text=type,
                command=self.master.title_pressed
            ))
            self.buttons[count].grid(
                row=count, 
                column=0,
                padx=PADDING
            )
            count += 1