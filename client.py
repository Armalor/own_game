import socket
from queue import Queue
from time import perf_counter
from statistics import mean, variance, stdev
from concurrent.futures import ThreadPoolExecutor, as_completed

# sock = socket.socket()
# sock.settimeout(2)
# sock.connect(('192.168.1.7', 9999))
#
# PING_SIZE = 5
# ping_q = Queue(maxsize=PING_SIZE)
#
# for i in range(10):
#     t0 = perf_counter()
#     sock.send(f'SYN {i}'.encode())
#
#     data = sock.recv(1024)
#     t1 = perf_counter() - t0
#     if ping_q.full():
#         _ = ping_q.get()
#     ping_q.put(t1)
#
#     avg = mean(ping_q.queue)
#
#     print(data.decode(), f'ping: {avg:.3f}')
#
# sock.close()
#


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


result = net_scan()
print(f'Результат {result}')
