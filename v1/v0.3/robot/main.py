"""
Robot-Dev Code Version 0.3.0-26032019
This code is design to be used with Raspberry Pi Zero W

*This code is to function as a slave following one master (server)
instructions.
*print function is used for debugging purposes.

"""
import RPi.GPIO as gpio
import selectors
import socket
import types
import time
import os

#Global variables
name = "Robot 1"

class DCMDirect(): # DC Motor Direct Voltage (No PWM)
    """
    For use with Motor Driver and 2 DC Motors.
    Voltage are supplied directly to the Motors.
    Dependencies: RPi.GPIO as gpio
    
    *Default RPi GPIO pin used:
        [(32,36) and (38,40)] based on BOARD ref.
        [(12,16) and (20,21)] based on Broadcom SOC Channel ref.
    
    *Please specify pin value and pin reference method when instantiating
    this class.
        Format: ( [M1+, M1-, M2+, M2-], gpio.BOARD or gpio.BCM )
        *use super().__init__(Format) if inheriting this class
    
    *Pin value and reference method can be change by using the build-in
    functions provided.
    *change_pin accept a list of pins as argument.
        Format: [M1+, M1-, M2+, M2-]
    *change_pin_ref only accepts either gpio.BOARD or gpio.BCM
                        
    See circuit_sketch.png for the circuitry

    """
    
    def __init__(self, pin=[32, 36, 38, 40], pin_ref="gpio.BOARD"):
        print("DCMDirect __init__ starts!")
        # Set default values
        self.pin_ref = pin_ref
        self.pin = pin
        
        # Set Pin Ref Mode
        gpio.setmode(self.pin_ref)
        
        # Setup Motor Pin I/O
        gpio.setup(self.pin[0], gpio.OUT, initial=gpio.LOW)
        gpio.setup(self.pin[1], gpio.OUT, initial=gpio.LOW)
        gpio.setup(self.pin[2], gpio.OUT, initial=gpio.LOW)
        gpio.setup(self.pin[3], gpio.OUT, initial=gpio.LOW)
        
    def change_pin(self, pin):
        # Making sure pin numbers doesn't exceed 40
        for each in pin:
            if pin <= 40:
                pass
            else:
                print("Failed to changed Motors pin!")
                return
        # Save new pin number
        self.pin = pin
        # Clean up previous setup
        gpio.cleanup()
        # Setup Motor Pin I/O
        gpio.setup(self.pin[0], gpio.OUT, initial=gpio.LOW)
        gpio.setup(self.pin[1], gpio.OUT, initial=gpio.LOW)
        gpio.setup(self.pin[2], gpio.OUT, initial=gpio.LOW)
        gpio.setup(self.pin[3], gpio.OUT, initial=gpio.LOW)
        print("Motors pin are now changed to", pin)
    
    def change_pin_ref(self, method):
        if method == "gpio.BOARD" or method == "gpio.BCM":
            print("Pin reference mode changed to", method)
            self.pin_ref = method
        else:
            print("Failed to change pin reference mode.")
        
    def forward(self):
        print("Moving forward!")
        gpio.output(self.pin[0], gpio.HIGH)
        gpio.output(self.pin[1], gpio.LOW)
        gpio.output(self.pin[2], gpio.HIGH)
        gpio.output(self.pin[3], gpio.LOW)
    
    def backwards(self):
        print("Moving backward!")
        gpio.output(self.pin[0], gpio.LOW)
        gpio.output(self.pin[1], gpio.HIGH)
        gpio.output(self.pin[2], gpio.LOW)
        gpio.output(self.pin[3], gpio.HIGH)
    
    def left(self):
        print("Rotate left!")
        gpio.output(self.pin[0], gpio.LOW)
        gpio.output(self.pin[1], gpio.HIGH)
        gpio.output(self.pin[2], gpio.HIGH)
        gpio.output(self.pin[3], gpio.LOW)
    
    def right(self):
        print("Rotate right!")
        gpio.output(self.pin[0], gpio.HIGH)
        gpio.output(self.pin[1], gpio.LOW)
        gpio.output(self.pin[2], gpio.LOW)
        gpio.output(self.pin[3], gpio.HIGH)
    
    def stop(self):
        print("Stop!")
        gpio.output(self.pin[0], gpio.LOW)
        gpio.output(self.pin[1], gpio.LOW)
        gpio.output(self.pin[2], gpio.LOW)
        gpio.output(self.pin[3], gpio.LOW)
        
    def __del__(self):
        # Cleanup GPIO after use to avoid improper GPIO setup later
        print("Cleaning up GPIO")
        gpio.cleanup()
        
class TCPHandler(): # TCP handler for incoming connection
    """
    Two way communication for multiple connections with multiplexing support.
    Dependencies: selectors, socket and types
    
    *Default port value is 5000 with a buffer size of 4096 bytes
    *To change the value, two arguments need to be pass to the class when
    inheriting or creating an instance.
    *Once initialize both variable are not changeable.
    
    """
    def __init__(self, port=5000, buf_size=4096):
        # Selectors for multiplexing
        self.sel = selectors.DefaultSelector()
        
        # Set buffer size
        self.buf_size = buf_size
        
        # Using IPv4
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.IP = self.get_self_IP()
        self.port = port
        self.bind((self.IP, self.port))
        self.sock.listen(32)
        self.sock.setblocking(False)
        self.sel.register(self.sock, selectors.EVENT_READ, data=None)
        
    def data_process(self, data):
        """
        To be define by user.
        Incoming stream is supposed to be 4096 bytes long.
        
        """
        pass
    
    def get_self_IP(self):
        try:
            self.sock.connect(("8.8.8.8", 80))
            IP = self.sock.getsockname()[0]
        except:
            IP = "127.0.0.1"
            print("Self IP set to", IP)
        finally:
            self.sock.close()
        return IP
    
    def accept_conn(self, sock):
        conn, addr = self.sock.accept()
        print("Accepted connection from", addr)
        conn.setblocking(False)
        data = type.SimpleNamespace(addr=addr, inb=b"", outb=b"")
        events = selectors.EVENT_READ | selectors.EVENT_WRITE
        self.sel.register(conn, events, data=data)
        
    def service_conn(self, key, mask):
        sock = key.fileobj
        data = key.data
        if mask & selectors.EVENT_READ:
            recv_data = self.sock.recv(self.buf_size)
            if recv_data:
                data.outb += recv_data
                self.data_process(recv_data)
            else:
                print("Closing connection to", data.addr)
                self.sel.unregister(sock)
                sock.close
        if mask & selectors.EVENT_WRITE:
            if data.outb:
                print("Echoing", repr(data.outb), "to", data.addr)
                sent = sock.send(data.outb)
                data.outb = data.outb[sent:]
                
    def check_conn(self):
        pass
    
class EasyLog():
    """
    A class for easily writing logs to a file named log_date
    Dependencies: time and os
    
    Please use the write_log function to start writing log.
    Please specify directory name when creating class if you want to change
    from the default log directory
    
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
        self.date = time.strftime("%d%m%Y") # Format: DayMonthYear [01012010]
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
            
    def write_log(self, text):
        # Get current date + time
        _date = time.ctime()
        # Prepare log text
        log_text = f"[ {_date} ]  {text}\n"
        if self.log_file:
            # Write log to file
            self.log_file.write(log_text)
            print(f"Writing '{text}' to {self.log_file_name}!")
        else:
            pass
        
    def close_log(self):
        # Properly close file after use
        self.log_file.close()
        print(f"Closing log {self.log_file_name}!")
            
    def __del__(self):
        self.close_log()
            

if __name__ == "__main__":
    pass

#     # For testing DCMDirect class
#     robot = DCMDirect()
#     robot.forward()
#     time.sleep(5)