import tkinter as tk

from constants import *

class GroupWindow(tk.Frame):
    def __init__(self, master, group_names, entry_parent=True):

        self.width = 200
        self.height = 240

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

        self.group_list.bind("<<ListboxSelect>>", self.on_click)
        if self.entry_parent:
            self.group_list.bind("<Double-1>", self.on_doubleclick)

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



    # Handlers

    def on_click(self, event):
        w = event.widget
        try:
            index = int(w.curselection()[0])
            self.selected = w.get(index)

        except IndexError:
            # somehow this function was called with no selection
            # ignore it and do nothing
            return

    def on_doubleclick(self, event):
        print("line 110 group_window.py: on_doubleclick executed")
        w = event.widget
        try:
            index = int(w.curselection()[0])
            self.selected = w.get(index)
            self.master.move_to_group(self.selected)
            self.window.destroy()

        except IndexError:
            print("Oops, index error")
            # somehow this function was called with no selection
            # ignore it and do nothing
            return

    def key_pressed(self, event):
        if event.keysym == "Return":
            self.add_group()



    def add_group(self):
        name = self.add_entry_var.get()

        if self.entry_parent:
            self.master.add_group(name)
        else:
            self.master.master.top_frame.add_group(name)

        self.add_entry.delete(0, tk.END)
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
            print(f"entry parent - groups: {groups}")
        else:
            groups = self.master.master.top_frame.get_group_names()
            print(f"non entry parent - groups: {groups}")
        self.list_var.set(groups)



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