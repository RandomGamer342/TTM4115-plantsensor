import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008

SPI_PORT   = 0
SPI_DEVICE = 0
mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))

"""
from RPi import GPIO
GPIO.VERBOSE = False # No debug printing from dummy GPIO library
GPIO.cleanup() # Set RPi GPIO to default to avoid causing hardware issues. No other program should be running on this device, so this is OK
GPIO.setmode(GPIO.BCM)
"""

class Sensor:
    def __init__(self, pin):
        self.pin = pin

    def read(self):
        return mcp.read_adc(self.pin)