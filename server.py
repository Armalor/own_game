from socketserver import ThreadingTCPServer, BaseRequestHandler
from time import perf_counter, sleep

from threading import Thread

# Локальный импорт:
import sys
from pathlib import Path
__root__ = Path(__file__).absolute().parent
sys.path.append(__root__.__str__())
from server import ConnectionHandler
# ~Локальный импорт

HOST, PORT = "", 9999


def serve():
    with ThreadingTCPServer((HOST, PORT), ConnectionHandler) as server:
        print('Start server')
        server.serve_forever()


if __name__ == "__main__":
    th = Thread(target=serve, daemon=True)
    th.start()

    while True:
        sleep(2)