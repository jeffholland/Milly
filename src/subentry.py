import tkinter as tk

from constants import *
from entry import Entry

class SubEntry(Entry):
    def __init__(self, date, time, text, width, height, index, master):

        Entry.__init__(
            date,
            time,
            text,
            width,
            height,
            index,
            self
        )

        self.master = master
