"""
Robot-Dev Code Version 0.6.0-29032019
This code is design to be used with Raspberry Pi Zero W

*This code is to function as a slave following one master (server)
instructions.
*print function is used for debugging purposes.
*log.write_log are use to keep record of the program

"""
# Direct import
import selectors
import socket
import types

# Partial import
from easylog import EasyLog
from dcmcontrol import DCMControl
from tcphandler import TCPHandler

# Global variables
name = "Robot 1"
log = EasyLog() # Initialize EasyLog

if __name__ == "__main__":
    pass