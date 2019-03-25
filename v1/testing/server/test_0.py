import socket
import time

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('192.168.1.17', 8485))
s.sendall(b"Hello World")
data = s.recv(1024)
s.close()
print("Received", repr(data))