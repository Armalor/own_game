from tkinter import *
from tkinter import ttk
from tkinter import font as tkFont

import socket
from queue import Queue
from time import perf_counter, sleep
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Thread
from statistics import mean


# Локальный импорт:
import sys
from pathlib import Path
__root__ = Path(__file__).absolute().parent
sys.path.append(__root__.__str__())
from classes import Wizard, Step, Net
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
                # одинаковый team_id == 17
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

class PlayGame(Step):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        for r in range(5):
            self.rowconfigure(index=r, weight=1)

        for c in range(4):
            self.columnconfigure(index=c, weight=1)

        self.canvas = Canvas(self, height=45)
        self.canvas.grid(in_=self, row=0, column=0, columnspan=4, sticky=NSEW)

        self.colors = {
            'norm': {
                'bg': 'green',
                'fill': '#ffffff',
            },
            'warn': {
                'bg': 'yellow',
                'fill': 'blue',
            },
            'alert': {
                'bg': 'red',
                'fill': '#ffffff',
            }
        }

        self.text_id = self.canvas.create_text(20, 60, anchor=NW, text=f'Connection...', font="Arial 28")

        # Кнопка готовности к ответу:
        s = ttk.Style()
        s.configure('my.TButton', font=('Arail', 36, 'bold'))

        self.btn = ttk.Button(self, text='GO!', width=50, style='my.TButton', state='disabled')

        self.btn.grid(in_=self, row=1, column=0, rowspan=4, columnspan=4, sticky=NSEW)

    def start(self):
        server_ip = Net.scan()

        th = Thread(target=self.ping, args=(server_ip,), daemon=True)
        th.start()

    def ping(self, server_ip):
        PING_SIZE = 10
        ping_q = Queue(maxsize=PING_SIZE)

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(2)
            sock.connect((server_ip, 9999))

            colors = {
                'norm': {
                    'bg': 'green',
                    'fill': '#ffffff',
                },
                'warn': {
                    'bg': 'yellow',
                    'fill': 'blue',
                },
                'alert': {
                    'bg': 'red',
                    'fill': '#ffffff',
                }
            }

            self.canvas["bg"] = colors['norm']['bg']
            self.btn['state'] = 'enabled'
            while True:
                t0 = perf_counter()
                sock.sendall(f'SYN_{self.controller.team_id}'.encode())

                data = sock.recv(1024)

                t1 = perf_counter() - t0
                if ping_q.full():
                    _ = ping_q.get()
                ping_q.put(t1)

                avg_ping = mean(ping_q.queue)

                if avg_ping < 0.005:
                    bg = colors['norm']['bg']
                    fill = colors['norm']['fill']
                elif avg_ping < 0.05:
                    bg = colors['warn']['bg']
                    fill = colors['warn']['fill']
                else:
                    bg = colors['alert']['bg']
                    fill = colors['alert']['fill']

                print(data.decode(), f'ping: {avg_ping:.5f}')

                self.canvas["bg"] = bg
                self.canvas.itemconfig(self.text_id, text=f"Team {self.controller.team_id}, ping: {avg_ping:.4f}", fill=fill)
                sleep(0.1)


if __name__ == "__main__":

    steps = [ChooseTeam, PlayGame]

    app = Wizard(title="Choose Team ID...", steps=steps)
    app.mainloop()