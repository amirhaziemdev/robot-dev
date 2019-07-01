"""
Created by: Ahmad Ammar Asyraaf Bin Jainuddin
Version: 1.1.1-09042019
Last Modified: 08:18 AM - 09/04/2019

"""
import RPi.GPIO as gpio
import time

class DCMControl():
    """
    For use with Motor Driver that supports PWM and 2 DC Motors.
    Dependencies: RPi.GPIO as gpio, time
    
    *Default Raspberry Pi GPIO pin used:
        [(32,36) and (38,40)] based on BOARD ref.
        [(12,16) and (20,21)] based on Broadcom SOC Channel ref.
    
    *Variables that can be specify when initiating this class is as follows:
        DCMControl(pin=[m1+,m1-,m2+,m2-],pin_ref="BOARD"/"BCM",freq=any,dc=any)
    
    *Pin value and reference method can be change by using the build-in
    functions provided.
    *change_pin accept a list of pins as argument. [List]
        Format: [M1+, M1-, M2+, M2-]
    *change_pin_ref only accepts either BOARD or BCM [String]
    *change_speed accepts number from 0 to 100 [%]
    *change_freq accepts any number [Hz]

    """
    
    def __init__(self, pin=[32, 36, 38, 40], pin_ref="BOARD", freq=100, dc=50):
        print("DCMControl __init__ starts!")
        # Creating variables and settings its values
        self.change_pin_ref(pin_ref)
        self.pin = pin
        self.freq = freq # PWM Freq
        self.dc = dc # PWM Duty Cycle
        self.move = False
        
        # Set Pin Reference Mode
        gpio.setmode(self.pin_ref)
        
        # Setup Motor Pin I/O
        self.change_pin(pin)
        
    def change_pin(self, pin):
        print("Changing Motors pin to", pin)
        # Making sure pin numbers doesn't exceed 40
        for each in pin:
            if 1 <= each <= 40:
                pass
            else:
                print("Failed to changed Motors pin!")
                return 1 # Signify error
        # Save new pin number
        self.pin = pin
        # Clean up previous setup
        try:
            gpio.cleanup()
        except:
            pass
        # Setup Motor Pin I/O
        gpio.setup(self.pin[0], gpio.OUT, initial=gpio.LOW)
        self.p0 = gpio.PWM(self.pin[0], self.freq)
        gpio.setup(self.pin[1], gpio.OUT, initial=gpio.LOW)
        self.p1 = gpio.PWM(self.pin[1], self.freq)
        gpio.setup(self.pin[2], gpio.OUT, initial=gpio.LOW)
        self.p2 = gpio.PWM(self.pin[2], self.freq)
        gpio.setup(self.pin[3], gpio.OUT, initial=gpio.LOW)
        self.p3 = gpio.PWM(self.pin[3], self.freq)
        print("Motors pin are now set to", pin)
        return 0 # Success
    
    def change_pin_ref(self, method):
        if method == "BOARD" or method == "BCM":
            print("Pin reference mode set to", method)
            if method == "BCM":
                self.pin_ref = gpio.BCM
            else:
                self.pin_ref = gpio.BOARD
            return 0 # Success
        else:
            print("Failed to change pin reference mode.")
            return 1 # Signify error
        
    def change_speed(self, dc):
        print("Changing motor speed to", dc, "%")
        if self.move == "False":
            self.dc = dc
            return 0
        else:
            try:
                self.p0.ChangeDutyCycle(dc)
                self.p1.ChangeDutyCycle(dc)
                self.p2.ChangeDutyCycle(dc)
                self.p3.ChangeDutyCycle(dc)
                return 0
            except:
                print("Error changing motor speed!")
                return 1
            
    def change_freq(self, freq):
        print("Changing PWM freq to", freq)
        try:
            self.p0.ChangeFrequency(freq)
            self.p1.ChangeFrequency(freq)
            self.p2.ChangeFrequency(freq)
            self.p3.ChangeFrequency(freq)
            return 0
        except:
            return 1
        
    def movement(self, direction):
        print("Moving", direction,"!!!")
        self.pwm_reset()
        self.move = True
        if direction == "forward":
            self._forward()
            return 0
        elif direction == "backwards":
            self._backwards()
            return 0
        elif direction == "left":
            self._left()
            return 0
        elif direction == "right":
            self._right()
            return 0
        else:
            self.move = False
            print("Failed to moved in", direction)
            return 1 # Error
        
    def _forward(self):
        gpio.output(self.pin[1], gpio.LOW)
        gpio.output(self.pin[3], gpio.LOW)
        self.p0.start(self.dc)
        self.p2.start(self.dc)
    
    def _backwards(self):
        gpio.output(self.pin[0], gpio.LOW)
        gpio.output(self.pin[2], gpio.LOW)
        self.p1.start(self.dc)
        self.p3.start(self.dc)
    
    def _left(self):
        gpio.output(self.pin[0], gpio.LOW)
        gpio.output(self.pin[3], gpio.LOW)
        self.p1.start(self.dc)
        self.p2.start(self.dc)
    
    def _right(self):
        gpio.output(self.pin[1], gpio.LOW)
        gpio.output(self.pin[2], gpio.LOW)
        self.p0.start(self.dc)
        self.p3.start(self.dc)
    
    def stop(self):
        print("Stop!!!")
        self.pwm_reset()
        self.move = False
        gpio.output(self.pin[0], gpio.LOW)
        gpio.output(self.pin[1], gpio.LOW)
        gpio.output(self.pin[2], gpio.LOW)
        gpio.output(self.pin[3], gpio.LOW)
        
    def pwm_reset(self):
        self.p0.stop()
        self.p1.stop()
        self.p2.stop()
        self.p3.stop()
        
    def __del__(self):
        # Cleanup GPIO after use to avoid improper GPIO setup later
        print("Cleaning up GPIO")
        self.pwm_reset()
        gpio.cleanup()
        
if __name__ == "__main__":
    # For testing DCMControl class
    robot = DCMControl()
    robot.movement("forward")
    time.sleep(5)