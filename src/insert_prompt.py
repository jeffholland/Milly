import tkinter as tk

from data import get_entries, insert_entry

class InsertPrompt(tk.Frame):
    def __init__(self, master):
        self.master = master
        self.window = tk.Toplevel(master)
        self.window.resizable(False, False)

        self.max_val = len(get_entries())

        self.create_widgets()

    def create_widgets(self):
        self.spinbox = tk.Spinbox(
            self.window,
            from_=0,
            to_=len(get_entries())
        )
        self.spinbox.grid(row=0, column=0)
        self.spinbox.focus_set()

        self.spinbox.bind("<KeyPress>", self.key_pressed)

    def key_pressed(self, event):
        if event.keysym == "Return":
            insert_entry(
                int(self.spinbox.get()), 
                self.master.input.get("1.0", "end")
            )
            self.master.master.refresh_entries()

            self.window.destroy()
            self.window.update()