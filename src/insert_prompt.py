import tkinter as tk
from tkinter import ttk

from constants import PLATFORM
from data import *

class InsertPrompt(tk.Frame):
    def __init__(self, master):
        self.master = master
        self.window = tk.Toplevel(master)
        self.window.resizable(False, False)

        self.max_val = get_num_entries

        self.create_widgets()



    def create_widgets(self):
        # Index to insert at
        self.spinbox = tk.Spinbox(
            self.window,
            from_=0,
            to_=get_num_entries()
        )
        self.spinbox.grid(row=0, column=0)
        self.spinbox.focus_set()
        self.spinbox.selection('to', tk.END)

        self.spinbox.bind("<KeyPress>", self.key_pressed)
        self.spinbox.bind("<KeyRelease>", self.key_released)

        # Select group to insert into
        self.group_var = tk.StringVar()

        vals = get_group_names()
        vals.insert(0, "None")
        self.group_var.set(vals[0])

        self.group_selector = ttk.Combobox(
            self.window,
            values=vals,
            textvariable=self.group_var,
            state="readonly",
            takefocus=0
        )
        self.group_selector.grid(row=1, column=0)



    def key_pressed(self, event):
        if event.keysym == "Return":
            insert_entry(
                int(self.spinbox.get()), 
                self.master.input.get("1.0", "end"),
                group=self.group_var.get()
            )
            self.master.input.delete("1.0", "end")
            self.master.master.refresh_entries()

            self.window.destroy()
            self.window.update()

    def key_released(self, event):
        # Release command key while in other window
        if PLATFORM == "Windows":
            if "Control" in event.keysym:
                self.master.key.keys_pressed["cmd"] = False
        else:
            if "Meta" in event.keysym:
                self.master.key.keys_pressed["cmd"] = False



    def refresh_colors(self, colors):
        self.colors = colors

        self.window.configure(
            bg=self.colors["BG2"]
        )

        self.spinbox.configure(
            bg=self.colors["BG1"],
            fg=self.colors["HL2"],
            highlightbackground=self.colors["HL1"],
            highlightcolor=self.colors["HL2"]
        )