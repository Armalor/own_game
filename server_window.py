from tkinter import *
from tkinter import ttk
from socketserver import ThreadingTCPServer
from threading import Thread

# Локальный импорт:
import sys
from pathlib import Path
__root__ = Path(__file__).absolute().parent
sys.path.append(__root__.__str__())
from server import ConnectionHandler
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


for r in range(1, 3):
    for c in range(8):
        canvas = Canvas(bg="#c0c0c0", height=45, width=45)
        canvas.grid(row=r, column=c*2, columnspan=2, sticky=NSEW)

start = ttk.Style()
start.configure('start.TButton', font=('Arail', 36, 'bold'))

clear = ttk.Style()
clear.configure('clear.TButton', font=('Arail', 28, 'bold'))

btn = ttk.Button(text="START", style='start.TButton')
btn.grid(row=5, column=0, columnspan=6, sticky=NSEW)

btn = ttk.Button(text="Clear", style='clear.TButton')
btn.grid(row=5, column=10, columnspan=6, sticky=NSEW)


canvas = Canvas(height=45, width=45)
canvas.grid(row=6, column=0, columnspan=16, sticky=NSEW)
canvas.create_text(512, 35, anchor=CENTER, text=f'Results:', fill='black', font="Arial 14")

for c in range(16):
    canvas = Canvas(bg="#c0c0c0", height=45, width=45)
    canvas.grid(row=7, column=c, sticky=NSEW)


HOST, PORT = "", 9999


def serve():
    with ThreadingTCPServer((HOST, PORT), ConnectionHandler) as server:
        print('Start server')
        server.serve_forever()


if __name__ == "__main__":
    th = Thread(target=serve, daemon=True)
    th.start()

    root.mainloop()
