import tkinter as tk

from constants import *

class Template(tk.Frame):
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

        self.labels = []
        self.buttons = []

        self.create_widgets()



    def create_widgets(self):
        self.window = tk.Toplevel(self)
        self.window.geometry(f"{self.width}x{self.height}")
        self.window.title("Template")
        self.window.overrideredirect(True)

        self.canvas_object_ids = []

        self.canvas = tk.Canvas(self.window)
        self.scrollbar = tk.Scrollbar(
            self.window,
            orient="vertical",
            command=self.canvas.yview,
            width=20,
            takefocus=0
        )
        self.canvas.configure(
            yscrollcommand=self.scrollbar.set
        )
        self.container = tk.Frame(self.canvas)
        self.canvas.grid(row=0, column=0)
        self.scroll_config()
        self.scrollbar.grid(
            row=0, 
            column=1, 
            sticky="ns"
        )

        self.canvas_object_ids.append(
            self.canvas.create_window(
                (0,0),
                window=self.container,
                anchor='nw'
            )
        )

        self.container.bind("<Configure>", self.scroll_config)
        self.container.bind("<Motion>", self.scroll_config)


    def scroll_config(self, event=None):
        self.canvas.configure(
            scrollregion=self.canvas.bbox("all"),
            width=self.width - 25,
            height=self.height
        )



    def refresh_colors(self, colors):
        self.colors = colors