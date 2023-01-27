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
                text=type
            ))
            self.configure_button(self.buttons[count], type)
            self.buttons[count].grid(
                row=count, 
                column=0,
                padx=PADDING
            )
            count += 1

    def configure_button(self, button, type):
        if type == self.widget_types[0]:
            button.configure(
                command=self.master.title_pressed
            )
        elif type == self.widget_types[1]:
            button.configure(
                command=self.master.icon_pressed
            )
        elif type == self.widget_types[2]:
            button.configure(
                command=self.master.number_pressed
            )
        elif type == self.widget_types[3]:
            button.configure(
                command=self.master.due_pressed
            )