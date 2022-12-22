import tkinter as tk

from constants import *

class ShowColorSchemes(tk.Frame):
    def __init__(self, master):

        self.width = 290
        self.height = 290

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
        # Template code
        self.window = tk.Toplevel(self)
        self.window.geometry(f"{self.width}x{self.height}")
        self.window.overrideredirect(True)

        # Scrollable template code
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

        # Actual code for this module

        self.bg1_frames = []
        self.bg2_frames = []
        self.hl1_frames = []
        self.hl2_frames = []

        self.color_schemes = self.master.master.master.colors_obj.get_color_schemes()
        for count in range(len(self.color_schemes)):

            # Get the color scheme dict (with all the hex codes)
            scheme = self.master.master.master.colors_obj.get_color_scheme(
                self.color_schemes[count]
            )

            # Create a label for the name
            self.labels.append(tk.Label(
                self.container,
                text=self.color_schemes[count],
                justify=tk.LEFT
            ))
            self.labels[count].grid(row=count,column=0)

            self.bg1_frames.append(tk.Frame(
                self.container,
                bg=scheme["BG1"],
                width=40,
                height=40
            ))
            self.bg1_frames[count].grid_propagate(0)
            self.bg1_frames[count].grid(row=count, column=1)

            self.bg2_frames.append(tk.Frame(
                self.container,
                bg=scheme["BG2"],
                width=40,
                height=40
            ))
            self.bg2_frames[count].grid_propagate(0)
            self.bg2_frames[count].grid(row=count, column=2)

            self.hl1_frames.append(tk.Frame(
                self.container,
                bg=scheme["HL1"],
                width=40,
                height=40
            ))
            self.hl1_frames[count].grid_propagate(0)
            self.hl1_frames[count].grid(row=count, column=3)

            self.hl2_frames.append(tk.Frame(
                self.container,
                bg=scheme["HL2"],
                width=40,
                height=40
            ))
            self.hl2_frames[count].grid_propagate(0)
            self.hl2_frames[count].grid(row=count, column=4)


    def scroll_config(self, event=None):
        self.canvas.configure(
            scrollregion=self.canvas.bbox("all"),
            width=self.width - 25,
            height=self.height
        )


    def refresh_colors(self, colors):
        self.colors = colors