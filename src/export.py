import tkinter as tk

import csv
from math import floor

from fpdf import FPDF

from colors import hex_to_rgb
from constants import *

class ExportWindow(tk.Frame):
    def __init__(self, master):

        self.width = 300
        self.height = 200

        tk.Frame.__init__(
            self,
            master,
            width=self.width,
            height=self.height
        )
        self.master = master

        self.buttons = []

        self.create_widgets()



    def create_widgets(self):

        # toplevel window

        self.window = tk.Toplevel(self)
        self.window.geometry(f"{self.width}x{self.height}")
        self.window.overrideredirect(True)



        # checkbuttons

        self.csv_var = tk.IntVar()
        self.csv_button = tk.Checkbutton(
            self.window,
            text="csv",
            variable=self.csv_var
        )
        self.csv_button.grid(row=0, column=0)
        self.buttons.append(self.csv_button)

        self.txt_var = tk.IntVar()
        self.txt_button = tk.Checkbutton(
            self.window,
            text="txt",
            variable=self.txt_var
        )
        self.txt_button.grid(row=1, column=0)
        self.buttons.append(self.txt_button)

        self.pdf_var = tk.IntVar()
        self.pdf_button = tk.Checkbutton(
            self.window,
            text="pdf",
            variable=self.pdf_var
        )
        self.pdf_button.grid(row=2, column=0)
        self.buttons.append(self.pdf_button)

        self.colors_var = tk.IntVar()
        self.colors_button = tk.Checkbutton(
            self.window,
            text="show colors",
            variable=self.colors_var
        )
        self.colors_button.grid(row=2, column=1)
        self.buttons.append(self.colors_button)

        for button in self.buttons:
            button.grid_configure(
                padx=PADDING,
                pady=PADDING
            )



        # filename entry

        self.filename_var = tk.StringVar()
        self.filename_entry = tk.Entry(
            self.window,
            textvariable=self.filename_var
        )
        self.filename_entry.grid(
            row=0, 
            column=1, 
            padx=PADDING, 
            pady=PADDING
        )
        self.filename_entry.focus_set()
        self.filename_entry.bind("<KeyPress>", self.key_pressed)



    def refresh_colors(self, colors):
        self.colors = colors

        self.window.configure(bg=self.colors["BG2"])

        for button in self.buttons:
            button.configure(
                highlightbackground=self.colors["HL1"],
                bg=self.colors["BG2"],
                fg=self.colors["HL2"]
            )

    

    def key_pressed(self, event):
        if event.keysym == "Return":
            self.export()


    def export(self):
        # Save everything to export folder
        filename = "export/" + self.filename_var.get()

        if self.csv_var.get() == 1:
            self.export_csv(filename)

        if self.txt_var.get() == 1:
            self.export_txt(filename)

        if self.pdf_var.get() == 1:
            self.export_pdf(filename)

        self.window.withdraw()


    def export_csv(self, filename):

        filename = filename + ".csv"

        with open(filename, "w") as csvfile:
            writer = csv.writer(csvfile, delimiter=",")
            for entry in self.master.entries:
                writer.writerow([entry.text])

    def export_txt(self, filename):
        filename = filename + ".txt"

        with open(filename, "w") as txtfile:
            for entry in self.master.entries:
                txtfile.write(entry.text)

    def export_pdf(self, filename):
        filename = filename + ".pdf"

        pdf = FPDF()
        pdf.add_page()
        pdf.set_font(ENTRY_FONT_FAMILY, size=ENTRY_FONT_SIZE)
        pdf.set_margins(PADDING, PADDING, PADDING)
        pdf.set_line_width(0.1)
        
        if self.colors_var.get() == 1:
            bg = hex_to_rgb(self.colors["BG2"])
            fg = hex_to_rgb(self.colors["HL2"])

            pdf.set_fill_color(bg[0], bg[1], bg[2])
            pdf.set_text_color(fg[0], fg[1], fg[2])
        
        for count in range(len(self.master.entries)):
            pdf.multi_cell(
                w=180,
                h=floor(self.master.entries[count].height / 4),
                txt=self.master.entries[count].text.strip(),
                border=1,
                fill=True
            )

        pdf.output(filename)