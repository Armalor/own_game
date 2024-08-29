from socketserver import ThreadingTCPServer, BaseRequestHandler
import re
from queue import Queue
from typing import Dict
from time import perf_counter, sleep
from statistics import mean


PING_SIZE = 5


class ConnectionHandler(BaseRequestHandler):

    PING_SIZE = 5

    def __init__(self, request, client_address, server):

        self.ping_queues: Dict[str, Queue] = dict()
        self.perf_counters: Dict[str, float] = dict()

        super().__init__(request, client_address, server)

    def handle(self):
        print("Connected by", self.client_address)
        while True:
            try:
                data = self.request.recv(1024)
            except ConnectionError:
                print(f"Client suddenly closed while receiving")
                break
            if not data:
                break

            data = data.decode()

            try:
                syn_pattern = re.search(r'^SYN_(?P<team_id>.+)$', data)
                if syn_pattern:
                    team_id = syn_pattern.group('team_id')

                    if team_id not in self.perf_counters:
                        self.perf_counters[team_id] = perf_counter()
                        self.ping_queues[team_id] = Queue(maxsize=self.PING_SIZE)
                    else:
                        ping_q = self.ping_queues[team_id]
                        t1 = perf_counter() - self.perf_counters[team_id]
                        if ping_q.full():
                            _ = ping_q.get()
                        ping_q.put(t1)
                        avg = mean(ping_q.queue)
                        print(f'team {team_id} ping: {avg:.5f}')
                        self.perf_counters[team_id] = perf_counter()

                    response = f'ACK_{team_id}'
                else:
                    response = f'ACK_???'

                # Искусственное циклическое изменение пинга:
                # cnt = (int(perf_counter()) // 10) % 3
                #
                # print(cnt)
                #
                # if cnt == 0:
                #     ...
                # elif cnt == 1:
                #     sleep(0.005)
                # else:
                #     sleep(0.05)

                self.request.sendall(response.encode())
            except ConnectionError:
                print(f"Client suddenly closed, cannot send")
                break
        print("Disconnected by", self.client_address)


HOST, PORT = "", 9999

if __name__ == "__main__":
    with ThreadingTCPServer((HOST, PORT), ConnectionHandler) as server:
        print('Start server')
        server.serve_forever()
