import socket

sock = socket.socket()
sock.bind(('', 9999))
sock.listen(1)
conn, addr = sock.accept()

while True:
    data = conn.recv(1024)
    if not data:
        conn.close()
        conn, addr = sock.accept()
        continue
    conn.send(b'ACK: ' + data)


