#!/usr/bin/env python

import socket


TCP_IP = '192.168.1.225'
TCP_PORT = 5005
BUFFER_SIZE = 1024
MESSAGE = b"s"

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
s.sendall(MESSAGE)
data = s.recv(BUFFER_SIZE)
print(data)
s.close()

print("received data:", data)

# f -forward
#b - backward
#l
#r
#s
#stop - to stop the program