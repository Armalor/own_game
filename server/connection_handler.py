from socketserver import ThreadingTCPServer, BaseRequestHandler
import re
from queue import Queue
from typing import Dict, List
from time import perf_counter, sleep
from statistics import mean
from threading import Lock
from enum import IntEnum, Enum
from dataclasses import dataclass
from collections import OrderedDict


# Локальный импорт:
import sys
from pathlib import Path
__root__ = Path(__file__).absolute().parent.parent
sys.path.append(__root__.__str__())
# ~Локальный импорт


class StateEnum(str, Enum):
    CLEAR = 'CLEAR'
    GO = 'GO'


class SignalEnum(str, Enum):
    SYN = 'SYN'
    GO = 'GO'


@dataclass
class GoTiming:
    team_id: int
    false_start: bool


class ConnectionHandler(BaseRequestHandler):

    PING_SIZE = 5

    PING_TIMING: Dict[int, float] = {k: 0 for k in range(1, 17)}
    GO_TIMING: Dict[int, GoTiming] = dict()
    LOCK = Lock()

    CLEAR_TAPS = 0

    # Изначальное состояние — «очистка». GO-сигнал в этом состоянии
    STATE = StateEnum.CLEAR

    def __init__(self, request, client_address, server):

        self.ping_queues: Dict[int, Queue] = dict()
        self.perf_counters: Dict[int, float] = dict()
        self.prev_state = self.STATE
        self.clear_taps = self.CLEAR_TAPS

        super().__init__(request, client_address, server)

    @classmethod
    def clear(cls):
        with cls.LOCK:
            cls.STATE = StateEnum.CLEAR
            cls.GO_TIMING = dict()
            cls.CLEAR_TAPS += 1

    @classmethod
    def go(cls):
        with cls.LOCK:
            cls.STATE = StateEnum.GO

    def go_response(self, team_id):
        with self.LOCK:
            go_timing = self.GO_TIMING.setdefault(team_id, GoTiming(team_id, self.STATE == StateEnum.CLEAR))

            if go_timing.false_start:
                response = f'GO_{team_id}_response_FS'
            else:
                go_timing_without_false_start = [k for k, v in self.GO_TIMING.items() if not v.false_start]
                place = go_timing_without_false_start.index(team_id) + 1
                response = f'GO_{team_id}_response_{place}'

        return response

    def ask_response(self, team_id):
        response = f'ASK_{team_id}'
        if (self.prev_state == StateEnum.GO and self.STATE == StateEnum.CLEAR) or (self.clear_taps < self.CLEAR_TAPS):
            # Если мы перешли из состояния «прием ответов» в «очистить старые результаты»,
            # ИЛИ просто еще раз нажали кнопку «Clear», то отдаем «Ready...»
            response = f'ASK_{team_id}_response_RD'
        elif self.prev_state == StateEnum.CLEAR and self.STATE == StateEnum.GO:
            # Если же наоборот, перешли в режим ожидания ответов, то отдаем GO!
            response = f'ASK_{team_id}_response_GO'

        self.prev_state = self.STATE
        self.clear_taps = self.CLEAR_TAPS
        return response

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
                pattern = re.search(r'^(?P<signal>SYN|GO)_(?P<team_id>\d+)$', data)

                if pattern:
                    team_id = int(pattern.group('team_id'))
                    signal = pattern.group('signal')

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
                        # print(f'team {team_id} ping: {avg:.5f}')
                        self.perf_counters[team_id] = perf_counter()

                    response = None

                    with self.LOCK:
                        self.PING_TIMING[team_id] = perf_counter()

                    if signal == SignalEnum.GO:
                        response = self.go_response(team_id)
                    elif signal == SignalEnum.SYN:
                        response = self.ask_response(team_id)

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

                    if response:
                        self.request.sendall(response.encode())



            except ConnectionError:
                print(f"Client suddenly closed, cannot send")
                break
        print("Disconnected by", self.client_address)