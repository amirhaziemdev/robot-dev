"""
Robot-Dev Code Version 0.3.0-26032019
This code is design to be used with a windows computer

*This code is to function as a master giving instruction to many slaves.
*print function is used for debugging purposes.

"""
import selectors
import socket
import types
import time
import os

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
    
class EasyLog():
    """
    A class for easily writing logs to a file named log_date
    Dependencies: time and os
    
    Please use the write_log function to start writing log.
    
    """
    def __init__(self, dir="log"):
        # Initialize variables
        self.date = ""
        self.log_file = ""
        self.dir = dir+"/"
        
        # Check for log directory, create one if doesn't exist
        try:
            os.listdir(self.dir)
        except:
            os.makedirs(self.dir)
        
        # Open log and ready for writing
        self.open_log()
    
    def get_todays_date(self):
        self.date = time.strftime("%d%m%Y")
        print("Fetching today's date!")
    
    def _open(self):
        # Get today's date
        self.get_todays_date()
        # Open log file/Create new if doesn't exist and ready to write
        self.log_file_name = "log_" + str(self.date)
        _log_dir = self.dir + self.log_file_name
        self.log_file = open(
            _log_dir,
            "a+",
            )
        print(f"Log file {self.log_file_name} has been opened!")
        
    def open_log(self):
        # Create new log file if different date, else pass
        if self.log_file:
            if self.date != time.strftime("%d%m%Y"):
                self._open()
            else:
                return
        else: # Create new log if one doesn't exist
            self._open()
    
    def close_log(self):
        self.log_file.close()
        print(f"Closing log {self.log_file_name}!")
            
    def write_log(self, text):
        _date = time.ctime()
        log_text = f"[ {_date} ]  {text}\n"
        if self.log_file:
            self.log_file.write(log_text)
            print(f"Writing '{text}' to {self.log_file_name}!")
        else:
            pass
            
    def __del__(self):
        self.close_log()