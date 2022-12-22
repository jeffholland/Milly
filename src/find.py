import tkinter as tk

from constants import *

class FindWindow(tk.Frame):
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

        self.window = tk.Toplevel(self.master)
        self.window.geometry(f"{self.width}x{self.height}")
        self.window.overrideredirect(True)

        self.entry_var = tk.StringVar()
        self.entry = tk.Entry(
            self.window,
            width=10,
            textvariable=self.entry_var
        )
        self.entry.grid(
            row=0, 
            column=0,
            padx=PADDING,
            pady=PADDING,
            columnspan=2
        )
        self.entry.bind("<KeyPress>", self.key_pressed)

        self.ok_button = tk.Button(
            self.window,
            text="Ok",
            command=self.ok_pressed
        )
        self.ok_button.grid(
            row=1,
            column=1,
            padx=PADDING,
            pady=PADDING
        )
        
        self.cancel_button = tk.Button(
            self.window,
            text="Cancel",
            command=self.cancel_pressed
        )
        self.cancel_button.grid(
            row=1,
            column=0,
            padx=PADDING,
            pady=PADDING
        )



    def refresh_colors(self, colors):
        self.colors = self.master.master.colors_obj.get_colors()

        self.window.configure(
            bg=self.colors["BG1"]
        )

        self.entry.configure(
            bg=self.colors["HL1"],
            fg=self.colors["BG2"]
        )


    def key_pressed(self, event):
        if event.keysym == "Return":
            self.ok_pressed()
        if event.keysym == "Escape":
            self.cancel_pressed()

    def ok_pressed(self):
        text = self.entry_var.get()
        self.master.master.top_frame.filter_entries(text)
        
        self.window.withdraw()
        self.master.input.focus_set()

    def cancel_pressed(self):
        self.window.withdraw()
        self.master.input.focus_set()