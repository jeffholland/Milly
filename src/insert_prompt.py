import tkinter as tk

from constants import PLATFORM
from data import insert_entry, get_num_entries

class InsertPrompt(tk.Frame):
    def __init__(self, master):
        self.master = master
        self.window = tk.Toplevel(master)
        self.window.resizable(False, False)

        self.max_val = get_num_entries

        self.create_widgets()

    def create_widgets(self):
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

    def key_pressed(self, event):
        if event.keysym == "Return":
            insert_entry(
                int(self.spinbox.get()), 
                self.master.input.get("1.0", "end")
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