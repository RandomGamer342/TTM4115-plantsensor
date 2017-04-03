import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008

#Wiring guide: https://learn.adafruit.com/raspberry-pi-analog-to-digital-converters/mcp3008
#RPi SPI port-out: https://pinout.xyz/pinout/spi
#Using the cobbler didn't seem to work, so connect the chip and components directly to the RPi for now
SPI_PORT   = 0
SPI_DEVICE = 0
mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))

class Sensor:
    def __init__(self, id, pin, maxthr):
        self.id = id
        self.pin = pin
        self.maxthr = maxthr
        print(f"Initialised sensor {id}.")

    def read(self):
        return min(float(mcp.read_adc(self.pin)) / self.maxthr, 1.)