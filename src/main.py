import tkinter as tk

from colors import Colors
from constants import *
from entries import Entries
from input import Input
from settings import Settings



class Application(tk.Frame):
    def __init__(self, master=None):

        tk.Frame.__init__(self, master)
        
        self.grid(row=0, column=0)

        if MODE == "fullscreen":
            self.width = self.winfo_screenwidth()
            self.height = self.winfo_screenheight()
        else:
            self.width = WIDTH
            self.height = HEIGHT

        self.colors_obj = Colors(self)
        
        self.create_widgets()
        self.refresh_colors()



    def create_widgets(self):

        # Settings initialized first

        self.settings = Settings(
            self, 
            width=self.width, 
            height=self.height
        )
        self.settings.grid_propagate(0)

        # Top frame is where entries are shown

        self.top_frame_height = (self.height // 3) * 2

        self.windows_offset = 110
        if PLATFORM == "Windows":
            self.top_frame_height += self.windows_offset

        self.top_frame = Entries(
            width=self.width, 
            height=self.top_frame_height,
            master=self)
        self.top_frame.grid_propagate(0)

        self.top_frame.grid(row=0, column=0)

        self.bottom_frame_height = self.height // 3
        if PLATFORM == "Windows":
            self.bottom_frame_height -= self.windows_offset

        # Bottom frame is where entries are input

        self.bottom_frame = Input(
            width=self.width,
            height=self.bottom_frame_height,
            master=self
        )
        self.bottom_frame.grid_propagate(0)

        self.bottom_frame.grid(row=1, column=0)

        # Settings applied after all other widgets created
        self.settings.apply_settings()



    def refresh_colors(self):
        self.colors = self.colors_obj.get_colors()

        self.top_frame.configure(bg=self.colors["HL1"])
        self.bottom_frame.configure(bg=self.colors["BG2"])
        self.settings.configure(bg=self.colors["BG1"])

        self.top_frame.refresh_colors()
        self.bottom_frame.refresh_colors()
        self.settings.refresh_colors()



    def refresh_entries(self):
        self.top_frame.refresh_entries()



    def show_settings(self):
        self.top_frame.grid_remove()
        self.bottom_frame.grid_remove()

        self.settings.grid(row=0, column=0)

    def hide_settings(self):
        self.settings.grid_remove()

        self.top_frame.grid()
        self.bottom_frame.grid()
        self.bottom_frame.input.focus_set()

        self.refresh_colors()

    def show_hide_checks(self):
        current = self.settings.entry_settings.show_checkboxes_var.get()
        if current == 0:
            self.settings.entry_settings.show_checkboxes_var.set(1)
        else:
            self.settings.entry_settings.show_checkboxes_var.set(0)
        self.settings.entry_settings.show_checkboxes_pressed()
        


app = Application()
app.master.title("Diary")
app.master.geometry(str(app.width) + "x" + str(app.height))
app.mainloop()