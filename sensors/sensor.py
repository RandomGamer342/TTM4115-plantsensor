from RPi import GPIO
GPIO.VERBOSE = False # No debug printing from dummy GPIO library
GPIO.cleanup() # Set RPi GPIO to default to avoid causing hardware issues. No other program should be running on this device, so this is OK
GPIO.setmode(GPIO.BCM)

class Sensor:
    def __init__(self, pin):
        self.pin = pin
        GPIO.setup(pin, GPIO.IN)

    def read(self):
        return GPIO.input(self.pin)