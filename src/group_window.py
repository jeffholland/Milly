import tkinter as tk
from tkinter import messagebox

from constants import *

class GroupWindow(tk.Frame):
    def __init__(self, master, group_names, entry_parent, entry_in_group=False):

        self.width = 200
        self.height = 280

        tk.Frame.__init__(
            self,
            master,
            width=self.width,
            height=self.height
        )
        self.master = master

        # If the "master" is an Entry object
        # (e.g. if an Entry's "group" button was pressed,
        # versus the general "Groups" button or cmd+g key shortcut)

        self.entry_parent = entry_parent

        # If entry parent, then is the entry in a group?
        # (Naturally this will be false if entry_parent is false)

        self.entry_in_group = entry_in_group

        self.group_names = group_names

        self.labels = []
        self.buttons = []

        self.selected = None

        self.create_widgets()



    def create_widgets(self):
        self.window = tk.Toplevel(self)
        self.window.geometry(f"{self.width}x{self.height}")

        self.list_var = tk.StringVar()
        self.refresh_groups()
        self.group_list = tk.Listbox(
            self.window,
            listvariable=self.list_var
        )
        self.group_list.grid(
            row=0,
            column=0,
            columnspan=5,
            padx=PADDING,
            pady=PADDING
        )

        # Event bindings

        self.group_list.bind("<<ListboxSelect>>", self.on_click)
        self.group_list.bind("<Double-1>", self.on_doubleclick)
        self.bind_all("<KeyRelease>", self.key_release)

        self.add_button = tk.Button(
            self.window,
            width=1,
            text="+",
            command=self.add_group
        )
        self.add_button.grid(
            row=1,
            column=0
        )
        self.buttons.append(self.add_button)

        self.delete_button = tk.Button(
            self.window,
            width=1,
            text="-",
            command=self.delete_group
        )
        self.delete_button.grid(
            row=1,
            column=1
        )
        self.buttons.append(self.delete_button)

        self.up_button = tk.Button(
            self.window,
            width=1,
            text="up",
            command=self.up_pressed
        )
        self.up_button.grid(
            row=2,
            column=0
        )
        self.buttons.append(self.up_button)

        self.down_button = tk.Button(
            self.window,
            width=1,
            text="down",
            command=self.down_pressed
        )
        self.down_button.grid(
            row=2,
            column=1
        )
        self.buttons.append(self.down_button)

        self.add_entry_var = tk.StringVar()
        self.add_entry = tk.Entry(
            self.window,
            width=5,
            textvariable=self.add_entry_var
        )
        self.add_entry.grid(
            row=1,
            column=2
        )
        self.add_entry.bind("<KeyPress>", self.key_pressed)
        self.add_entry.focus_set()
        self.add_entry.select_range(start=0, end=tk.END)



    # Handlers

    def on_click(self, event=None):
        self.get_selection()

    def on_doubleclick(self, event=None):
        if self.entry_parent:
            self.get_selection()
            self.master.move_to_group(self.selected_index)
            self.window.destroy()
        else:
            self.get_selection()
            self.master.submit(group_index=self.selected_index)
            self.window.destroy()

    def key_pressed(self, event):
        if event.keysym == "Return":
            self.add_group()
        if event.keysym == "Up":
            try:
                index = self.group_list.curselection()[0]
                index = index - 1
                self.group_list.selection_clear(0, tk.END)
                self.group_list.selection_set(index, index)
            except IndexError:
                pass
        if event.keysym == "Down":
            try:
                index = self.group_list.curselection()[0]
                index = index + 1
                self.group_list.selection_clear(0, tk.END)
                self.group_list.selection_set(index, index)
            except IndexError:
                print("index error")
                pass
                

    def key_release(self, event):
        # Release command key while in other window
        if PLATFORM == "Windows":
            if "Control" in event.keysym:
                if self.entry_parent:
                    self.master.master.master.master.master.bottom_frame.key.keys_pressed["cmd"] = False
                else:
                    self.master.key.keys_pressed["cmd"] = False
        else:
            if "Meta" in event.keysym:
                if self.entry_parent:
                    if self.entry_in_group:
                        self.master.master.master.master.master.master.bottom_frame.key.keys_pressed["cmd"] = False
                    else:
                        self.master.master.master.master.master.bottom_frame.key.keys_pressed["cmd"] = False
                else:
                    self.master.key.keys_pressed["cmd"] = False


    def add_group(self):
        name = self.add_entry_var.get()

        if name in self.group_names:
            # If group already exists, act as though the group
            # were double-clicked.
            self.on_doubleclick()
            return

        # Call entries object add group function
        if self.entry_parent:
            self.master.add_group(name)
        else:
            self.master.master.top_frame.add_group(name)

        # Clear all text from the entry
        self.add_entry.delete(0, tk.END)

        # Refresh the displayed list
        self.refresh_groups()

    def delete_group(self):
        if self.selected:
            if self.entry_parent:
                self.master.delete_group(self.selected)
            else:
                self.master.master.top_frame.delete_group(self.selected)
            self.refresh_groups()

    def refresh_groups(self):
        if self.entry_parent:
            groups = self.master.get_group_names()
        else:
            groups = self.master.master.top_frame.get_group_names()
        self.list_var.set(groups)

    def up_pressed(self):
        if self.entry_parent:
            self.master.move_group(self.selected, "up")
        else:
            self.master.master.top_frame.move_group(self.selected, "up")
        self.refresh_groups()

    def down_pressed(self):
        if self.entry_parent:
            self.master.move_group(self.selected, "down")
        else:
            self.master.master.top_frame.move_group(self.selected, "down")
        self.refresh_groups()



    def refresh_colors(self, colors):
        self.colors = colors

        self.window.configure(
            bg=self.colors["BG1"]
        )
        
        self.group_list.configure(
            bg=self.colors["BG2"],
            fg=self.colors["HL2"]
        )

        self.add_entry.configure(
            bg=self.colors["HL1"],
            fg=self.colors["BG1"],
            highlightbackground=self.colors["BG2"],
            highlightcolor=self.colors["HL2"]
        )

        for button in self.buttons:
            button.configure(
                highlightbackground=self.colors["BG1"]
            )
            if PLATFORM == "Windows":
                button.configure(
                    bg=self.colors["BG2"],
                    fg=self.colors["HL2"]
                )

    # Utility for setting selection

    def get_selection(self):
        try:
            index = int(self.group_list.curselection()[0])
            self.selected = self.group_list.get(index)
            self.selected_index = index

        except IndexError:
            # if DEBUG:
            #     messagebox.showerror("group_window IndexError", "group_window.py get_selection caught an IndexError")
            return

        except tk.TclError:
            if DEBUG:
                messagebox.showerror("group_window TclError", "group_window caught a TclError")
            return

        self.add_entry_var.set(self.selected)
        self.add_entry.select_range(start=0, end=tk.END)