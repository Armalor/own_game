from tkinter import *
from tkinter import ttk

import socket
from queue import Queue
from time import perf_counter, sleep
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Thread
from statistics import mean

TEAM_NUMBER = 1


def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(0)
    try:
        # doesn't even have to be reachable
        s.connect(('10.254.254.254', 1))
        ip = s.getsockname()[0]
    finally:
        s.close()

    return ip.split('.')


def find_server(ip):
    sock = socket.socket()
    sock.settimeout(2)
    try:
        sock.connect((ip, 9999))
    except (TimeoutError, ConnectionRefusedError):
        return False
    finally:
        sock.close()
    return ip


def net_scan():
    local_ip = get_local_ip()
    futures = list()
    result = False
    with ThreadPoolExecutor(max_workers=255) as executor:

        for d in range(1, 255):
            local_ip[-1] = f'{d}'
            futures.append(executor.submit(find_server, '.'.join(local_ip)))

        for future in as_completed(futures):
            result = future.result()
            if result:
                break

    return result


def ping(server_ip: str, team_id, canvas):
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

        canvas["bg"] = colors['norm']['bg']

        # btn["text"] = f"Connected to {server_ip}"
        text1 = canvas.create_text(20, 10, anchor=NW, text=f'ping: ', fill=colors['norm']['fill'], font="Arial 14")

        while True:
            t0 = perf_counter()
            sock.sendall(f'SYN_{team_id}'.encode())

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

            # print(data.decode(), f'ping: {avg_ping:.5f}')

            canvas["bg"] = bg
            canvas.itemconfig(text1, text=f"ping: {avg_ping:.4f}", fill=fill)
            sleep(0.1)
            # canvas1.delete(text1)


def click(canvas):
    if not hasattr(click, 'clicked'):
        click.clicked = True

        server_ip = net_scan()

        th = Thread(target=ping, args=(server_ip, TEAM_NUMBER, canvas), daemon=True)
        th.start()


def finish(root_):
    root_.destroy()  # ручное закрытие окна и всего приложения
    print("Закрытие приложения")


if __name__ == '__main__':
    def finish():
        root.destroy()  # ручное закрытие окна и всего приложения
        print("Закрытие приложения")

    root = Tk()
    root.title(f"Team #{TEAM_NUMBER}")
    root.geometry("1024x768")
    root.iconbitmap(default="favicon.ico")
    root.protocol("WM_DELETE_WINDOW", finish)
    # root.attributes("-fullscreen", True)

    canvas_ping = Canvas(bg="white", height=45)
    canvas_ping.pack(anchor='n', expand=True, fill=X)

    btn = ttk.Button(text="Find server...",  command=lambda: click(canvas_ping))
    btn.pack(anchor=CENTER, expand=True, ipadx=10, ipady=10)

    root.mainloop()

