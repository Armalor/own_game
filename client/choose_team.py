from tkinter import *
from tkinter import ttk

# Локальный импорт:
import sys
from pathlib import Path
__root__ = Path(__file__).absolute().parent.parent
sys.path.append(__root__.__str__())
from classes import Step
# ~Локальный импорт


class ChooseTeam(Step):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        for r in range(5):
            self.rowconfigure(index=r, weight=1)

        for c in range(4):
            self.columnconfigure(index=c, weight=1)

        label = ttk.Label(self, text="Choose Team ID", font='Arial 14', anchor=CENTER)
        label.grid(in_=self, row=0, column=0, columnspan=4, sticky=NSEW)

        team_id = 1
        for r in range(1, 5):
            for c in range(0, 4):
                # Если передавать не так, а через command=lambda: self.next(team_id), то у всех команд будет
                # одинаковый team_id == 17 (последнее значение)

                btn = ttk.Button(self, text=team_id, width=50, command=self.next(team_id))
                btn.grid(in_=self, row=r, column=c, sticky=NSEW)

                team_id += 1

    def next(self, team_id=None):
        """Если передавать не так, а через lambda, то у всех команд будет одинаковый team_id == 17"""
        nxt = super().next

        def ret():
            self.controller.team_id = team_id
            nxt()

        return ret
