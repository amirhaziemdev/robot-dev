import RPi.GPIO as gpio

# Set pin using BCM
gpio.setmode(gpio.BCM)

# Set pin IO
gpio.setup(14, gpio.OUT)
gpio.setup(15, gpio.OUT)
gpio.setup(20, gpio.OUT)
gpio.setup(21, gpio.OUT)

gpio.output(14, gpio.LOW)
gpio.output(15, gpio.LOW)
gpio.output(21, gpio.LOW)
gpio.output(20, gpio.LOW)
