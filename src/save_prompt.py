import tkinter as tk

from sys import exit

from constants import *

class SavePrompt(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(
            self, 
            master
        )

        self.window = tk.Toplevel(
            master
        )
        self.window.title("Save prompt")
        self.window.geometry("250x100")
        if PLATFORM == "Windows":
            self.window.geometry("200x100")

        self.buttons = []

        self.create_widgets()



    def create_widgets(self):
        self.label = tk.Label(
            self.window,
            text="Would you like to save changes?"
        )
        self.label.grid(
            row=0,
            column=0,
            columnspan=3,
            padx=PADDING,
            pady=PADDING
        )

        self.yes_button = tk.Button(
            self.window,
            text="Yes",
            command=self.yes_pressed
        )
        self.yes_button.grid(
            row=1,
            column=0,
            padx=PADDING,
            pady=PADDING
        )
        self.yes_button.focus_set()
        self.buttons.append(self.yes_button)

        self.no_button = tk.Button(
            self.window,
            text="No",
            command=self.no_pressed
        )
        self.no_button.grid(
            row=1,
            column=1,
            padx=PADDING,
            pady=PADDING
        )
        self.buttons.append(self.no_button)

        self.cancel_button = tk.Button(
            self.window,
            text="Cancel",
            command=self.cancel_pressed
        )
        self.cancel_button.grid(
            row=1,
            column=2,
            padx=PADDING,
            pady=PADDING
        )
        self.buttons.append(self.cancel_button)

        self.bind_all("<KeyRelease>", self.key_released)



    def refresh_colors(self, colors):
        self.colors = colors

        self.window.configure(
            bg=self.colors["BG2"]
        )

        self.label.configure(
            bg=self.colors["BG2"],
            fg=self.colors["HL2"],
        )
        
        for button in self.buttons:
            button.configure(
                highlightbackground=self.colors["BG2"],
                highlightcolor=self.colors["HL2"]
            )
            if PLATFORM == "Windows":
                button.configure(
                    bg=self.colors["BG1"],
                    fg=self.colors["HL2"]
                )

    def yes_pressed(self):
        self.master.save(and_exit=True)

    def no_pressed(self):
        exit()

    def cancel_pressed(self):
        self.window.destroy()



    def key_released(self, event):
        # Release command key while in other window
        if PLATFORM == "Windows":
            if "Control" in event.keysym:
                self.master.key.keys_pressed["cmd"] = False
        else:
            if "Meta" in event.keysym:
                self.master.key.keys_pressed["cmd"] = False