import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont

from constants import *

class FontSettings(tk.Frame):
    def __init__(self, master):

        tk.Frame.__init__(
            self,
            master,
            width=WIDTH - PADDING_BIG * 2, 
            height=120
        )
        self.master = master

        self.labels = []
        self.buttons = []

        self.create_widgets()



    def create_widgets(self):

        self.title_label = tk.Label(
            self,
            text="Font",
            justify=tk.CENTER
        )
        self.title_label.grid(
            row=0,
            column=0,
            columnspan=10
        )
        self.labels.append(self.title_label)

        self.font_family_var = tk.StringVar()
        self.font_family_selector = ttk.Combobox(
            self,
            state="readonly",
            textvariable=self.font_family_var
        )
        self.font_family_selector.grid(
            row=1, 
            column=0,
            padx=PADDING,
            pady=PADDING
        )
        self.font_family_selector["values"] = tkFont.families()
        self.font_family_selector.bind(
            "<<ComboboxSelected>>", 
            self.font_selected
        )
        self.font_family_var.set("Helvetica")

        self.font_arrow_left = tk.Button(
            self,
            text="<<",
            command=lambda: self.arrow_pressed("left")
        )
        self.font_arrow_left.grid(
            row=1,
            column=1,
            padx=PADDING,
            pady=PADDING
        )
        self.buttons.append(self.font_arrow_left)

        self.font_arrow_right = tk.Button(
            self,
            text=">>",
            command=lambda: self.arrow_pressed("right")
        )
        self.font_arrow_right.grid(
            row=1,
            column=2,
            padx=PADDING,
            pady=PADDING
        )
        self.buttons.append(self.font_arrow_right)

        self.example_text = "AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz"

        self.font_example = tk.Label(
            self,
            text=self.example_text,
            font=tkFont.Font(self, family=self.font_family_var.get(), size=12)
        )
        self.font_example.grid(
            row=2,
            column=0,
            padx=PADDING,
            pady=PADDING,
            columnspan=5
        )
        self.labels.append(self.font_example)

        self.apply_font = tk.Button(
            self,
            text="Apply",
            command=self.apply_pressed
        )
        self.apply_font.grid(
            row=1,
            column=3,
            padx=PADDING,
            pady=PADDING
        )
        self.buttons.append(self.apply_font)


    def arrow_pressed(self, dir):
        families = tkFont.families()
        index = families.index(self.font_family_var.get())

        if dir == "left":
            if index > 0:
                self.font_family_var.set(families[index - 1])
            else:
                self.font_family_var.set(families[len(families) - 1])
        else:
            if index < len(families) - 1:
                self.font_family_var.set(families[index + 1])
            else:
                self.font_family_var.set(families[0])

        self.font_selected()


    def apply_pressed(self):
        font = tkFont.Font(
            self, 
            family=self.font_family_var.get(), 
            size=14
        )
        self.master.settings_data["font_family"] = self.font_family_var.get()
        self.master.master.top_frame.set_font(font)


    def font_selected(self, event=None):
        font = tkFont.Font(self, family=self.font_family_var.get(), size=12)
        self.show_font_example(font)


    def show_font_example(self, font):
        self.font_example.grid_remove()

        self.font_example.configure(font=font)
        self.font_example.grid()
        self.refresh_colors(self.colors)



    def refresh_colors(self, colors):
        self.colors = colors

        self.configure(
            bg=self.colors["BG2"]
        )

        for label in self.labels:
            if label:
                label.configure(
                    bg=self.colors["BG2"],
                    fg=self.colors["HL2"]
                )

        for button in self.buttons:
            button.configure(
                highlightbackground=self.colors["BG2"]
            )
            if PLATFORM == "Windows":
                button.configure(
                    bg=self.colors["BG1"],
                    fg=self.colors["HL2"]
                )