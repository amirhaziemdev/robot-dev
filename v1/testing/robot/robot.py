import RPi.GPIO as gpio
import time
import socket

# Set up TCP
TCP_IP = '192.168.1.225'
TCP_PORT = 5005
BUFFER_SIZE = 20  # Normally 1024, but we want fast response

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))

# Set Pin Ref Mode
gpio.setmode(gpio.BCM)

# Setup Pin I/O
gpio.setup(12, gpio.OUT, initial=gpio.LOW)
gpio.setup(16, gpio.OUT, initial=gpio.LOW)
gpio.setup(20, gpio.OUT, initial=gpio.LOW)
gpio.setup(21, gpio.OUT, initial=gpio.LOW)

# Internal Functions
def forward():
	gpio.output(12, gpio.HIGH)
	gpio.output(16, gpio.LOW)
	gpio.output(20, gpio.HIGH)
	gpio.output(21, gpio.LOW)

def backward():
	gpio.output(12, gpio.LOW)
	gpio.output(16, gpio.HIGH)
	gpio.output(20, gpio.LOW)
	gpio.output(21, gpio.HIGH)

def left():
	gpio.output(12, gpio.LOW)
	gpio.output(16, gpio.HIGH)
	gpio.output(20, gpio.HIGH)
	gpio.output(21, gpio.LOW)

def right():
	gpio.output(12, gpio.HIGH)
	gpio.output(16, gpio.LOW)
	gpio.output(20, gpio.LOW)
	gpio.output(21, gpio.HIGH)

def stop():
	gpio.output(12, gpio.LOW)
	gpio.output(16, gpio.LOW)
	gpio.output(20, gpio.LOW)
	gpio.output(21, gpio.LOW)

# Variables
quit = False

# Main Loop
while True:
	s.listen(1)
	conn, addr = s.accept()
	print("Connection from: ", addr)
	while 1:
		data = conn.recv(BUFFER_SIZE)
		if not data: break
		print("received data:", data)
		if data == "f":
			forward()
		elif data == "b":
			backward()
		elif data == "l":
			left()
		elif data == "r":
			right()
		elif data == "s":
			stop()
		elif data == "stop":
			quit = True
		conn.send(data)
	conn.close()
	if quit:
		break
gpio.cleanup()
