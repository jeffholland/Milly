import tkinter as tk
from tkinter import messagebox

from os import listdir, mkdir, rename, rmdir, remove
from os.path import isfile
from shutil import rmtree

from constants import *

class InputPathBrowser(tk.Frame):
    def __init__(self, master):

        tk.Frame.__init__(self, master.window)
        
        self.master = master

        self.buttons = []

        self.browser_shown = False

        self.name_window = None

        self.selected = None
        
        self.create_widgets()



    def create_widgets(self):

        # File browser - only shows when Browse button is pressed

        self.browser_var = tk.StringVar()
        self.browser = tk.Listbox(
            self.master.window,
            listvariable=self.browser_var,
            width=18
        )

        # Buttons that only show with the File browser

        self.new_folder_button = tk.Button(
            self.master.window,
            text="New folder",
            width=5,
            command=self.new_folder
        )
        self.buttons.append(self.new_folder_button)

        self.new_file_button = tk.Button(
            self.master.window,
            text="New file",
            width=4,
            command=self.new_file
        )
        self.buttons.append(self.new_file_button)

        self.rename_button = tk.Button(
            self.master.window,
            text="Rename",
            width=3,
            command=self.rename
        )
        self.buttons.append(self.rename_button)

        self.delete_button = tk.Button(
            self.master.window,
            text="Delete",
            width=3,
            command=self.delete
        )
        self.buttons.append(self.delete_button)

        self.browser.bind("<<ListboxSelect>>", self.on_click)
        self.browser.bind("<Double-1>", self.on_doubleclick)



    def show_browser(self, override=False):

        if (not self.browser_shown or override):
            files = self.list_files(self.master.load_path)

            # Add a back button if we are not at root save folder
            if self.master.load_path != SAVE_DATA_PATH:
                files.insert(0, "(back)")

            for file in list(files):
                # Remove hidden files
                if file[0] == ".":
                    files.remove(file)

            self.browser_var.set(files)

            self.browser.grid(
                row=1,
                column=0,
                columnspan=2,
                rowspan=4,
                padx=PADDING,
                pady=PADDING
            )

            count = 1
            for button in self.buttons:
                button.grid(row=count, column=2)
                count += 1

            self.master.window.geometry("280x280")
            
            self.browser_shown = True

        else:
            self.browser.grid_remove()
            for button in self.buttons:
                button.grid_remove()

            self.master.reset_window()
            self.browser_shown = False



    # Single click to select a json file (populates Entry widget)
    def on_click(self, event):
        w = event.widget
        try:
            index = int(w.curselection()[0])
            self.selected = w.get(index)

            # If not a directory (therefore a json file)
            # and also not the back button
            if self.selected[-1] != "/" and self.selected != "(back)":
                self.master.entry_var.set(self.selected)
        except IndexError:
            # somehow this function was called with no selection
            # ignore it and do nothing
            return

    # Double click to select file or enter directory
    def on_doubleclick(self, event):
        w = event.widget
        try:
            index = int(w.curselection()[0])
            self.selected = w.get(index)
            # Select directory
            if self.selected[-1] == "/":
                # List files in this directory (back button at the top)
                self.master.load_path = self.master.load_path + self.selected
                self.selecteds = self.list_files(self.master.load_path)
                self.selecteds.insert(0, "(back)")
                self.browser_var.set(self.selecteds)
            # Select back button
            if self.selected == "(back)":
                self.master.load_path = SAVE_DATA_PATH
                self.browser_var.set(self.list_files(self.master.load_path))
            # Select file (not directory or back button)
            if self.selected[-1] != "/" and self.selected != "(back)":
                # File already selected in entry box, so we can just submit
                self.master.submit()
        except IndexError:
            # somehow this function was called with no selection
            # ignore it and do nothing
            return



    # Utility for getting a list of files in a path,
    # formatted to my liking
    
    def list_files(self, path):
        # Filter .json files
        files = []
        for file in listdir(path):
            # json file - remove .json extension
            if file[-5:] == ".json":
                files.append(file[:-5])
            # directory - add a > symbol
            else:
                files.append(file + "/")

        files.sort()
        return files


    # Button handlers

    def new_folder(self):
        self.show_name_window(mode="new_folder")

    def new_folder_submit(self):
        path = self.master.load_path + self.name_entry.get()

        try:
            mkdir(path)
        except FileExistsError:
            messagebox.showinfo("folder already exists",
                "The folder you tried to create already exists.")
            pass

        self.hide_name_window()



    def new_file(self):
        self.show_name_window(mode="new_file")

    def new_file_submit(self):
        path = self.master.load_path + self.name_entry.get()

        if isfile(path):
            messagebox.showerror("file already exists",
                "The file you tried to create already exists")
        else:
            open(path + ".json", "w")

        self.hide_name_window()



    def rename(self):
        try:
            index = self.browser.curselection()[0]
            self.selected = self.browser.get(index)
        except IndexError:
            messagebox.showinfo("rename without selection",
                "Please select a folder or file to rename.")
            return
        self.show_name_window(mode="rename")

    def rename_submit(self):

        if self.selected[-1] == "/":
            # rename directory
            old_path = self.master.load_path + self.selected
            new_path = self.master.load_path + self.name_entry.get()
        else:
            # rename json file
            old_path = self.master.load_path + self.selected + ".json"
            new_path = self.master.load_path + self.name_entry.get() + ".json"
            self.master.entry_var.set(self.name_entry.get())

        rename(old_path, new_path)

        self.hide_name_window()



    def delete(self):
        try:
            index = self.browser.curselection()[0]
            self.selected = self.browser.get(index)
            path = self.master.load_path + self.selected

            if path[-1] == "/":
                # Remove directory
                if len(listdir(path)) == 0:
                    # Remove empty directory
                    rmdir(path)
                else:
                    # Remove directory with files
                    rmtree(path)
            else:
                # Remove json file
                remove(path + ".json")

        except IndexError:
            messagebox.showinfo("delete without selection",
                "Please select a folder or file to delete.")
            return

        self.show_browser(override=True)



    # Name window, used for creating and renaming files and folders

    def show_name_window(self, mode):
        self.name_window_mode = mode

        self.name_window = tk.Toplevel(self)
        self.name_window.geometry("100x50")

        self.name_entry = tk.Entry(
            self.name_window, 
            width=8
        )
        self.name_entry.grid(
            row=0, 
            column=0, 
            padx=PADDING, 
            pady=PADDING
        )
        self.name_entry.bind("<KeyPress>", self.name_entry_key_pressed)
        self.name_entry.focus_set()

    def hide_name_window(self):
        self.name_window.destroy()
        self.name_window = None

        self.show_browser(override=True)
        self.master.window.deiconify()

    def name_entry_key_pressed(self, event):
        if event.keysym == "Return":
            if self.name_window_mode == "new_folder":
                self.new_folder_submit()
            elif self.name_window_mode == "new_file":
                self.new_file_submit()
            elif self.name_window_mode == "rename":
                self.rename_submit()

    def refresh_colors(self, colors):
        self.colors = colors

        for button in self.buttons:
            button.configure(
                highlightbackground=self.colors["BG1"]
            )