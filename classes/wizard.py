import tkinter as tk
from tkinter import ttk, NSEW
from typing import List, Type

# Локальный импорт:
import sys
from pathlib import Path
__root__ = Path(__file__).absolute().parent.parent
sys.path.append(__root__.__str__())
from classes.step import Step
# ~Локальный импорт


class Wizard(tk.Tk):
    def __init__(self, title, steps: List[Type[Step]], *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title(title)
        self.geometry("1024x768")

        # Create a container to hold wizard frames
        self.container = ttk.Frame(self)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.current_step = 0
        self.steps = []

        for _Step in steps:
            step = _Step(self.container, self)
            step.grid(row=0, column=0, sticky=NSEW)
            self.steps.append(step)

        self.show_step(self.current_step)

        # TODO: метод, видимо, надо не «finish», а «destroy», плюс бежать по ВСЕМ шагам.
        self.protocol("WM_DELETE_WINDOW", self.steps[-1].finish)

    def show_step(self, step_idx: int):
        step = self.steps[step_idx]
        step.tkraise()
        step.start()

    def next(self):
        if self.current_step < len(self.steps)-1:
            self.current_step += 1
            self.show_step(self.current_step)

    def back(self):
        if self.current_step > 0:
            self.current_step -= 1
            self.show_step(self.current_step)


if __name__ == "__main__":

    steps = []


    class Step1(Step):
        def __init__(self, parent, controller):
            super().__init__(parent, controller)

            label = ttk.Label(self, text="Step 1")
            label.pack(pady=10, padx=10)
            button = ttk.Button(self, text="Next", command=controller.next)
            button.pack()


    class Step2(Step):
        def __init__(self, parent, controller):
            super().__init__(parent, controller)

            label = ttk.Label(self, text="Step 2")
            label.pack(pady=10, padx=10)
            button = ttk.Button(self, text="Next", command=controller.next)
            button.pack()
            button = ttk.Button(self, text="Back", command=controller.back)
            button.pack()


    class Step3(Step):
        def __init__(self, parent, controller):
            super().__init__(parent, controller)

            label = ttk.Label(self, text="Step 3")
            label.pack(pady=10, padx=10)
            button = ttk.Button(self, text="Back", command=controller.back)
            button.pack()

    steps.append(Step1)
    steps.append(Step2)
    steps.append(Step3)

    app = Wizard(title="test", steps=steps)
    app.mainloop()