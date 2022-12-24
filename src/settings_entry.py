import tkinter as tk

from constants import *

class EntrySettings(tk.Frame):
    def __init__(self, master):
        self.master = master

        tk.Frame.__init__(
            self,
            master,
            width=WIDTH - PADDING_BIG * 2, 
            height=120
        )

        self.labels = []
        self.buttons = []

        self.create_widgets()



    def create_widgets(self):

        self.title_label = tk.Label(
            self,
            text="Entry",
            justify=tk.CENTER
        )
        self.title_label.grid(
            row=0,
            column=0,
            columnspan=10
        )
        self.labels.append(self.title_label)

        self.show_checkboxes_var = tk.IntVar()
        self.show_checkboxes = tk.Checkbutton(
            self,
            text="Show checkboxes",
            variable=self.show_checkboxes_var,
            command=self.show_checkboxes_pressed
        )
        self.show_checkboxes.grid(
            row=1, 
            column=0,
            padx=PADDING,
            pady=PADDING
        )
        self.buttons.append(self.show_checkboxes)

        self.show_dates_var = tk.IntVar()
        self.show_dates = tk.Checkbutton(
            self,
            text="Show dates",
            variable = self.show_dates_var,
            command = self.show_dates_pressed
        )
        self.show_dates.grid(
            row=1, 
            column=1,
            padx=PADDING,
            pady=PADDING
        )
        self.buttons.append(self.show_dates)

        self.show_times_var = tk.IntVar()
        self.show_times = tk.Checkbutton(
            self,
            text="Show times",
            variable = self.show_times_var,
            command = self.show_times_pressed
        )
        self.show_times.grid(
            row=1, 
            column=2,
            padx=PADDING,
            pady=PADDING
        )
        self.buttons.append(self.show_times)

        self.show_menu_var = tk.IntVar()
        self.show_menu = tk.Checkbutton(
            self,
            text="Show menu",
            variable = self.show_menu_var,
            command = self.show_menu_pressed
        )
        self.show_menu.grid(
            row=1, 
            column=3,
            padx=PADDING,
            pady=PADDING
        )
        self.buttons.append(self.show_menu)



    def refresh_colors(self, colors):
        self.colors = colors

        self.configure(
            bg=self.colors["BG2"]
        )

        for label in self.labels:
            label.configure(
                bg=self.colors["BG2"],
                fg=self.colors["HL2"]
            )

        for button in self.buttons:
            button.configure(
                highlightbackground=self.colors["BG2"],
                bg=self.colors["BG2"],
                fg=self.colors["HL2"]
            )



    def show_checkboxes_pressed(self):
        v = self.show_checkboxes_var.get()

        self.master.settings_data["show_checkboxes"] = v

        if (v == 1):
            self.master.master.top_frame.show_checkboxes = True
            self.master.master.top_frame.refresh_entries()
        else:
            self.master.master.top_frame.show_checkboxes = False
            self.master.master.top_frame.refresh_entries()

    def show_dates_pressed(self):
        v = self.show_dates_var.get()

        self.master.settings_data["show_dates"] = v

        if (v == 1):
            self.master.master.top_frame.set_show_dates(True)
        else:
            self.master.master.top_frame.set_show_dates(False)

    def show_times_pressed(self):
        v = self.show_times_var.get()

        self.master.settings_data["show_times"] = v

        if (v == 1):
            self.master.master.top_frame.set_show_times(True)
        else:
            self.master.master.top_frame.set_show_times(False)

    def show_menu_pressed(self):
        v = self.show_menu_var.get()

        self.master.settings_data["show_menu"] = v

        if (v == 1):
            self.master.master.top_frame.show_menu = True
            self.master.master.top_frame.refresh_entries()
        else:
            self.master.master.top_frame.show_menu = False
            self.master.master.top_frame.refresh_entries()