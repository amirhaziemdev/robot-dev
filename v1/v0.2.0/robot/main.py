"""
Robot-Dev Code Version 0.2.0-25032019
This code is design to be used with Raspberry Pi Zero W

This code is to function as a slave following one master (server) instructions

"""
import RPi.GPIO as gpio
import selectors
import socket
import time

#Global variables
name = "Robot 1"

class DCMDirect(): # DC Motor Direct Voltage (No PWM)
    """
    For use with Motor Driver and 2 DC Motors
    Voltage are supplied directly to the Motors
    RPi GPIO pin used:  [(self.pin[0],36) and (self.pin[2],40)] based on BOARD ref.
                        [(12,16) and (20,21)] based on Broadcom SOC Channel ref.
                        
    Pin value can be change by overwriting DCMotorMovement attributes values.
    Please change value first before initializing if you don't want to use the default value
    pin_ref for reference mode
    pin with a format of [M1+, M1-, M2+, M2-] for pin connection to DC Motor
                        
    See circuit_sketch.png for the circuitry
    
    """
    pin_ref = gpio.BOARD
    pin = [ 32, 36, 38, 40]
    
    def __init__(self):
        # Get current attributes value
        self.pin_ref = DCMDirect.pin_ref
        self.pin = DCMDirect.pin
        
        # Set Pin Ref Mode
        gpio.setmode(self.pin_ref)
        
        # Setup Motor Pin I/O
        gpio.setup(self.pin[0], gpio.OUT, initial=gpio.LOW)
        gpio.setup(self.pin[1], gpio.OUT, initial=gpio.LOW)
        gpio.setup(self.pin[2], gpio.OUT, initial=gpio.LOW)
        gpio.setup(self.pin[3], gpio.OUT, initial=gpio.LOW)
        
    def forward(self):
        gpio.output(self.pin[0], gpio.HIGH)
        gpio.output(self.pin[1], gpio.LOW)
        gpio.output(self.pin[2], gpio.HIGH)
        gpio.output(self.pin[3], gpio.LOW)
    
    def backwards(self):
        gpio.output(self.pin[0], gpio.LOW)
        gpio.output(self.pin[1], gpio.HIGH)
        gpio.output(self.pin[2], gpio.LOW)
        gpio.output(self.pin[3], gpio.HIGH)
    
    def left(self):
        gpio.output(self.pin[0], gpio.LOW)
        gpio.output(self.pin[1], gpio.HIGH)
        gpio.output(self.pin[2], gpio.HIGH)
        gpio.output(self.pin[3], gpio.LOW)
    
    def right(self):
        gpio.output(self.pin[0], gpio.HIGH)
        gpio.output(self.pin[1], gpio.LOW)
        gpio.output(self.pin[2], gpio.LOW)
        gpio.output(self.pin[3], gpio.HIGH)
    
    def stop(self):
        gpio.output(self.pin[0], gpio.LOW)
        gpio.output(self.pin[1], gpio.LOW)
        gpio.output(self.pin[2], gpio.LOW)
        gpio.output(self.pin[3], gpio.LOW)
        
    def __del__(self):
        # Cleanup GPIO after use to avoid improper GPIO setup later
        gpio.cleanup()
        
class TCPHandler(): # TCP handler for incoming connection
    def __init__(self, port):
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

if __name__ == "__main__":
    pass

#     # For testing DCMDirect class
#     robot = DCMDirect()
#     robot.forward()
#     time.sleep(5)