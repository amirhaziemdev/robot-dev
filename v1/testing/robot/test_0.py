import selectors
import socket
import time

sel = selectors.DefaultSelector()

def accept(sock, mask):
    if mask == 0:
        print("0")
        return
    conn, addr = sock.accept()
    print("Connected from", addr)
    conn.setblocking(False)
    sel.register(conn, selectors.EVENT_READ, read)
    
def read(conn, mask):
    data = conn.recv(1024)
    if data:
        print("Echoing", repr(data), "to", conn.getpeername())
        conn.sendall(data)
    else:
        print("Closing connection from", conn.getpeername())
        sel.unregister(conn)
        conn.close()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('192.168.1.17', 8485))
s.listen(100)
s.setblocking(False)
sel.register(s, selectors.EVENT_READ, accept)
print("Listening on port 8485")

while True:
    events = sel.select(timeout=0)
    for key, mask in events:
        callback = key.data
        callback(key.fileobj, mask)