import selectors
import socket
import time

class RobotMaster():
    pass

class TCPHandler():
    def __init__(self):
        # Using IPv4
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)