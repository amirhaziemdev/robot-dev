"""
Robot-Dev Code Version 0.6.0-29032019
This code is design to be used with a windows computer

*This code is to function as a master giving instruction to many slaves.
*print function is used for debugging purposes.

"""
import selectors
import socket
import types

from easylog import EasyLog
from tcphandler import TCPHandler

class RobotMaster():
    pass