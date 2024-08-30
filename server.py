from tkinter import *
from tkinter import ttk
from socketserver import ThreadingTCPServer
from threading import Thread
from time import sleep, perf_counter
from typing import Dict, List

# Локальный импорт:
import sys
from pathlib import Path
__root__ = Path(__file__).absolute().parent
sys.path.append(__root__.__str__())
from server import ConnectionHandler, GoTiming
# ~Локальный импорт

root = Tk()
root.title("SERVER")
root.geometry("1024x768")


root.rowconfigure(index=0, weight=1)
root.columnconfigure(index=0, weight=8)
canvas = Canvas(height=45, width=45)
canvas.grid(row=0, column=0, columnspan=16, sticky=NSEW)
canvas.create_text(512, 35, anchor=CENTER, text=f'Connections:', fill='black', font="Arial 14")

for r in range(1, 3):
    root.rowconfigure(index=r, weight=1)

root.rowconfigure(index=4, weight=2)
root.rowconfigure(index=5, weight=30)
root.rowconfigure(index=6, weight=1)
root.rowconfigure(index=7, weight=1)
root.rowconfigure(index=8, weight=1)


for c in range(16):
    root.columnconfigure(index=c, weight=1)

connection_canvas = {}
team_id = 1
for r in range(1, 3):
    for c in range(8):
        connection_canvas[team_id] = Canvas(bg="#c0c0c0", height=45, width=45)
        connection_canvas[team_id].grid(row=r, column=c*2, columnspan=2, sticky=NSEW)
        connection_canvas[team_id].create_text(10, 10, anchor=NW, text=team_id, font="Arial 10", tags=['team_id'])
        team_id += 1

start = ttk.Style()
start.configure('start.TButton', font=('Arail', 36, 'bold'))

clear = ttk.Style()
clear.configure('clear.TButton', font=('Arail', 28, 'bold'))

btn = ttk.Button(text="GO!", style='start.TButton', command=ConnectionHandler.go)
btn.grid(row=5, column=0, columnspan=6, sticky=NSEW)

btn = ttk.Button(text="Clear", style='clear.TButton', command=ConnectionHandler.clear)
btn.grid(row=5, column=10, columnspan=6, sticky=NSEW)


canvas = Canvas(height=45, width=45)
canvas.grid(row=6, column=0, columnspan=16, sticky=NSEW)
canvas.create_text(512, 35, anchor=CENTER, text=f'Results:', fill='black', font="Arial 14")

result_canvas = []
team_id = 1
for c in range(16):
    canvas = Canvas(bg="#c0c0c0", height=45, width=45)
    canvas.create_text(20, 20, anchor=NW, text='', font="Arial 14", tags=['team_id'])
    canvas.grid(row=7, column=c, sticky=NSEW)
    result_canvas.append(canvas)



def shutdown(server):
    print('Stop server...')
    server.shutdown()
    print('Stopped')
    root.destroy()


def serve(server):
    with server:
        print('Start server')
        server.serve_forever(poll_interval=0.05)


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
    },
    'empty': {
        'bg': '#c0c0c0',
        'fill': 'black',
    },
}


def connection_checker(connection_canvas: Dict[int, Canvas]):
    while True:
        current_pc = perf_counter()
        # Делаем копию и БЫСТРО освобождаем защелку:
        with ConnectionHandler.LOCK:
            ping_timing = {k: v for k, v in ConnectionHandler.PING_TIMING.items()}

        for k, v in ping_timing.items():
            text_id = connection_canvas[k].find_withtag("team_id")[0]
            if v > 0:
                if current_pc - v < 0.5:
                    connection_canvas[k]['bg'] = colors['norm']['bg']
                    connection_canvas[k].itemconfig(text_id, fill=colors['norm']['fill'])
                elif current_pc - v < 1:
                    connection_canvas[k]['bg'] = colors['warn']['bg']
                    connection_canvas[k].itemconfig(text_id, fill=colors['warn']['fill'])
                elif current_pc - v < 120:
                    connection_canvas[k]['bg'] = colors['alert']['bg']
                    connection_canvas[k].itemconfig(text_id, fill=colors['alert']['fill'])
                else:
                    connection_canvas[k]['bg'] = colors['empty']['bg']
                    connection_canvas[k].itemconfig(text_id, fill=colors['empty']['fill'])
        sleep(0.5)


def results_checker(result_canvas: List[Canvas]):
    while True:
        # Делаем копию и БЫСТРО освобождаем защелку:
        with ConnectionHandler.LOCK:
            go_timing: Dict[int, GoTiming] = {k: v for k, v in ConnectionHandler.GO_TIMING.items()}

        if not go_timing:
            for canvas in result_canvas:
                canvas['bg'] = colors['empty']['bg']
                text_id = canvas.find_withtag("team_id")[0]
                canvas.itemconfig(text_id, text='', fill=colors['empty']['fill'])
        else:
            for idx, result in enumerate(go_timing.values(), start=0):
                color = 'alert' if result.false_start else 'norm'
                canvas = result_canvas[idx]
                text_id = canvas.find_withtag("team_id")[0]

                canvas['bg'] = colors[color]['bg']
                canvas.itemconfig(text_id, text=result.team_id, fill=colors[color]['fill'])

        sleep(0.5)


HOST, PORT = "", 9999

if __name__ == "__main__":
    server = ThreadingTCPServer((HOST, PORT), ConnectionHandler)
    th_serve = Thread(target=serve, args=(server,), daemon=True)
    th_serve.start()

    th_connection_checker = Thread(target=connection_checker, args=(connection_canvas,), daemon=True)
    th_connection_checker.start()

    th_results_checker = Thread(target=results_checker, args=(result_canvas,), daemon=True)
    th_results_checker.start()

    root.protocol("WM_DELETE_WINDOW", lambda: shutdown(server))
    root.mainloop()
