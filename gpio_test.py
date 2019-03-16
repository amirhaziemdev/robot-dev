#!/usr/bin/env python

import socket
from time import sleep

TCP_IP = '192.168.1.225'
TCP_PORT = 5005
BUFFER_SIZE = 1024

class Robot():
    def __init__(self, ip_addr, port, buffer_size):
        self.ip = ip_addr
        self.port = port
        self.buffer = buffer_size
        self.connect()
        self.delay = 10
        
        while True:
            self.routine()
    
    def routine(self):
        self.move_backwards()
        sleep(1)
        self.move_left()
        sleep(3)
        self.move_forward()
        sleep(1)
    
    def move_right(self):
        self.message = b"r"
        self.send_message()
        
    def move_left(self):
        self.message = b"l"
        self.send_message()
        
    def move_forward(self):
        self.message = b"f"
        self.send_message()
        
    def move_backwards(self):
        self.message = b"b"
        self.send_message()
        
    def stop(self):
        self.message = b"s"
        self.send_message()
    
    def connect(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.ip, self.port))
        
    def send_message(self):
        self.socket.sendall(self.message)
        data = self.socket.recv(self.buffer)
         
    def __del__(self):
#         self.message = b"stop"
#         self.send_message()
        self.stop()
        self.socket.close()



if __name__ == "__main__":
    Robot(TCP_IP, TCP_PORT, BUFFER_SIZE)

# f -forward
#b - backward
#l
#r
#s
#stop - to stop the program