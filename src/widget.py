import tkinter as tk

class Widget(tk.Frame):
    def __init__(self, master, width, height):

        tk.Frame.__init__(
            self, 
            master, 
            width=width, 
            height=height
        )

        self.master = master
        self.width = width
        self.height = height

        self.create_widgets()

    def create_widgets(self):
        self.title_label = tk.Label(
            self,
            text="Widget"
        )
        self.title_label.grid(row=0, column=0)

    def refresh_colors(self, colors):
        self.colors = colors
        
        self.configure(bg=colors["BG2"])