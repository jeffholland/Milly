import tkinter as tk

import csv
from math import floor

from fpdf import FPDF

from colors import hex_to_rgb
from constants import *

class ExportWindow(tk.Frame):
    def __init__(self, master):

        self.width = 300
        self.height = 160

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
        self.csv_var.set(1)
        self.csv_button = tk.Checkbutton(
            self.window,
            text="csv",
            variable=self.csv_var
        )
        self.csv_button.grid(row=0, column=0)
        self.buttons.append(self.csv_button)

        self.txt_var = tk.IntVar()
        self.txt_var.set(1)
        self.txt_button = tk.Checkbutton(
            self.window,
            text="txt",
            variable=self.txt_var
        )
        self.txt_button.grid(row=1, column=0)
        self.buttons.append(self.txt_button)

        self.pdf_var = tk.IntVar()
        self.pdf_var.set(1)
        self.pdf_button = tk.Checkbutton(
            self.window,
            text="pdf",
            variable=self.pdf_var
        )
        self.pdf_button.grid(row=2, column=0)
        self.buttons.append(self.pdf_button)

        self.colors_var = tk.IntVar()
        self.colors_var.set(1)
        self.colors_button = tk.Checkbutton(
            self.window,
            text="show colors",
            variable=self.colors_var
        )
        self.colors_button.grid(row=2, column=1)
        self.buttons.append(self.colors_button)

        self.dates_var = tk.IntVar()
        self.dates_var.set(1)
        self.dates_button = tk.Checkbutton(
            self.window,
            text="show dates",
            variable=self.dates_var
        )
        self.dates_button.grid(row=1, column=1)
        self.buttons.append(self.dates_button)
        if not self.master.show_dates:
            self.dates_button.configure(state=tk.DISABLED)

        self.times_var = tk.IntVar()
        self.times_var.set(1)
        self.times_button = tk.Checkbutton(
            self.window,
            text="show times",
            variable=self.times_var
        )
        self.times_button.grid(row=1, column=2)
        self.buttons.append(self.times_button)
        if not self.master.show_times:
            self.times_button.configure(state=tk.DISABLED)

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
            pady=PADDING,
            columnspan=2
        )
        self.filename_entry.focus_set()
        self.filename_entry.bind("<KeyPress>", self.key_pressed)
        self.filename_entry.bind("<KeyRelease>", self.key_released)



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

    def key_released(self, event):
        # Release command key while in other window
        if PLATFORM == "Windows":
            if "Control" in event.keysym:
                self.master.master.bottom_frame.key.keys_pressed["cmd"] = False
        else:
            if "Meta" in event.keysym:
                self.master.master.bottom_frame.key.keys_pressed["cmd"] = False


    def export(self):
        # Save everything to export folder
        filename = EXPORT_PATH + self.filename_var.get()

        if self.csv_var.get() == 1:
            self.export_csv(filename)

        if self.txt_var.get() == 1:
            self.export_txt(filename)

        if self.pdf_var.get() == 1:
            self.export_pdf(filename)

        self.window.withdraw()
        self.master.master.bottom_frame.input.focus_set()



    def export_csv(self, filename):

        filename = filename + ".csv"

        with open(filename, "w") as csvfile:
            writer = csv.writer(csvfile, delimiter=",")

            for group in self.master.groups:
                for entry in group.entries:
                    writer.writerow(self.get_csv_row(entry, group))
            
            for entry in self.master.ungrouped_entries:
                writer.writerow(self.get_csv_row(entry))

    def get_csv_row(self, entry, group=None):
        row = []

        if self.dates_var.get() == 1:
            row.append(entry.date)
        if self.times_var.get() == 1:
            row.append(entry.time)

        if group:
            row.append(group.name)
            
        row.append(entry.text)

        return row

                

    def export_txt(self, filename):
        filename = filename + ".txt"

        with open(filename, "w") as txtfile:
            for group in self.master.groups:
                for entry in group.entries:
                    txtfile.write(self.get_txt_row(entry, group))

            for entry in self.master.ungrouped_entries:
                txtfile.write(self.get_txt_row(entry))

    def get_txt_row(self, entry, group=None):
        row = ""

        if self.dates_var.get() == 1:
            row += entry.date + " - "
        if self.times_var.get() == 1:
            row += entry.time + " - "
        row += entry.text

        if group:
            row += " - " + group.name

        if row[-1] != '\n':
            row += '\n'

        return row



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

        for group in self.master.groups:
            for entry in group.entries:
                row = self.get_txt_row(entry, group=group)
                self.write_pdf_row(pdf, row, entry.height)
        
        for entry in self.master.ungrouped_entries:
            row = self.get_txt_row(entry)
            self.write_pdf_row(pdf, row, entry.height)

        pdf.output(filename)

    def write_pdf_row(self, pdf, row, height):
        fill = False
        if self.colors_var.get() == 1:
            fill = True

        pdf.multi_cell(
            w=180,
            h=floor(height / 4),
            txt=row,
            border=1,
            fill=fill
        )