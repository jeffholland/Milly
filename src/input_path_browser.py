import tkinter as tk

from os import listdir

from constants import *

class InputPathBrowser(tk.Frame):
    def __init__(self, master):

        tk.Frame.__init__(self, master.window)
        
        self.master = master

        self.buttons = []

        self.browser_shown = False
        
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



    def show_browser(self):

        if not self.browser_shown:
            self.browser_var.set(self.list_files(SAVE_DATA_PATH))

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
            value = w.get(index)
            # If not a directory (therefore a json file)
            if value[-1] != "/":
                self.master.entry_var.set(value)
        except IndexError:
            # no selection, nothing to do
            return

    # Double click to select file or enter directory
    def on_doubleclick(self, event):
        w = event.widget
        try:
            index = int(w.curselection()[0])
            value = w.get(index)
            # Select directory
            if value[-1] == "/":
                # List files in this directory (back button at the top)
                self.master.load_path = self.master.load_path + value
                values = self.list_files(self.master.load_path)
                values.insert(0, "(back)")
                self.browser_var.set(values)
            # Select back button
            if value == "(back)":
                self.master.load_path = SAVE_DATA_PATH
                self.browser_var.set(self.list_files(self.master.load_path))
            # Select file (not directory or back button)
            if value[-1] != "/" and value != "(back)":
                # File already selected in entry box, so we can just submit
                self.master.submit()
        except IndexError:
            # no selection, nothing to do
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
        print("new folder")

    def rename(self):
        try:
            index = self.browser.curselection()[0]
            print(self.browser.get(index))
        except IndexError:
            print("nothing to rename")
            # no selection, nothing to do
            return

    def delete(self):
        try:
            index = self.browser.curselection()[0]
            print(self.browser.get(index))
        except IndexError:
            print("nothing to delete")
            # no selection, nothing to do
            return