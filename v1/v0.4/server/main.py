"""
Robot-Dev Code Version 0.3.0-26032019
This code is design to be used with a windows computer

*This code is to function as a master giving instruction to many slaves.
*print function is used for debugging purposes.

"""
import selectors
import socket
import types

from easylog import EasyLog

class RobotMaster():
    pass

class TCPHandler():
    def __init__(self):
        # Using IPv4
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.IP = self.get_self_IP()
        self.port = port
        self.bind((self.IP, self.port))
    
    def get_self_IP(self):
        try:
            self.sock.connect(("8.8.8.8", 80))
            IP = self.sock.getsockname()[0]
        except:
            IP = "127.0.0.1"
        finally:
            self.sock.close()
        return IP