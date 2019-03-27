import RPi.GPIO as gpio

class DCMControl(): # DC Motor Direct Voltage (No PWM)
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
        print("DCMControl __init__ starts!")
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
        print(f"Changing Motors pin to {pin}")
        # Making sure pin numbers doesn't exceed 40
        for each in pin:
            if pin <= 40:
                pass
            else:
                print("Failed to changed Motors pin!")
                return 1 # Signify error
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
        return 0 # Success
    
    def change_pin_ref(self, method):
        if method == "gpio.BOARD" or method == "gpio.BCM":
            print("Pin reference mode changed to", method)
            self.pin_ref = method
            return 0 # Success
        else:
            print("Failed to change pin reference mode.")
            return 1 # Signify error
        
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
        
if __name__ == "__main__":
    # For testing DCMControl class
    robot = DCMControl()
    robot.forward()
    time.sleep(5)