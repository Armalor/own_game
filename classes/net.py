import socket
from concurrent.futures import ThreadPoolExecutor, as_completed


class Net:

    @staticmethod
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

    @staticmethod
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

    @staticmethod
    def scan():
        local_ip = Net.get_local_ip()
        futures = list()
        result = False
        with ThreadPoolExecutor(max_workers=255) as executor:

            for d in range(1, 255):
                local_ip[-1] = f'{d}'
                futures.append(executor.submit(Net.find_server, '.'.join(local_ip)))

            for future in as_completed(futures):
                result = future.result()
                if result:
                    break

        return result
