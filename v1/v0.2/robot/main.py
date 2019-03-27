"""
Robot-Dev Code Version 0.2.1-26032019
This code is design to be used with Raspberry Pi Zero W

*This code is to function as a slave following one master (server)
instructions.
*print function is used for debugging purposes.

"""
import RPi.GPIO as gpio
import selectors
import socket
import time

#Global variables
name = "Robot 1"

class DCMDirect(): # DC Motor Direct Voltage (No PWM)
    """
    For use with Motor Driver and 2 DC Motors.
    Voltage are supplied directly to the Motors.
    RPi GPIO pin used:
        [(32,36) and (38,40)] based on BOARD ref.
        [(12,16) and (20,21)] based on Broadcom SOC Channel ref.
                        
    *Pin value and reference method can be change by using the build-in
    functions provided.
    *change_pin accept a list of pins as argument.
        Format: [M1+, M1-, M2+, M2-]
    *change_pin_ref only accepts either gpio.BOARD or gpio.BCM
                        
    See circuit_sketch.png for the circuitry

    """
    
    def __init__(self):
        print("DCMDirect __init__ starts!")
        # Set default values
        self.pin_ref = gpio.BOARD
        self.pin = [
                32, 36, # Pin for DC Motor 1
                38, 40, # Pin for DC Motor 2
                ]
        
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
    Two way communication for multiple connections with multiplexing support
    Please specify port number that is going to be use for the communication
    when instantiating this class!
    The port specify is used for listening to connection.
    Use the connect_to() function to connect to other client.
    
    """
    def __init__(self, port):
        # Selectors for multiplexing
        self.sel = selectors.DefaultSelector()
        
        # Using IPv4
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.IP = self.get_self_IP()
        self.port = port
        self.bind((self.IP, self.port))
        self.sock.listen(100)
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
            recv_data = self.sock.recv(4096)
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
    
    

if __name__ == "__main__":
    pass

#     # For testing DCMDirect class
#     robot = DCMDirect()
#     robot.forward()
#     time.sleep(5)