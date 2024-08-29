from tkinter import *
from tkinter import ttk


class Step(ttk.Frame):
    def __init__(self, parent, controller):
        self.controller = controller
        super().__init__(parent)

    def next(self):
        self.controller.next()

    def back(self):
        self.controller.back()

    def start(self):
        pass

    def finish(self):
        pass