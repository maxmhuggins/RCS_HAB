import ADC
import SPI
import TEMP
import RPi.GPIO as RGPIO
#=====================================================#
"""                                                   
This section is only here to enable the output enable 
(OE) pin on a level shifter.                          
"""                                                   

OE = 26

RGPIO.setmode(RGPIO.BCM)
RGPIO.setup(OE, RGPIO.OUT)
RGPIO.output(OE, True)
#=====================================================#

SPI_PORT   = 0
SPI_DEVICE = 0
mcp = ADC.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))
ADC.ReferenceVoltage = 5.12

while True:
    d = mcp.read_adc(0)
    voltage = ADC.getVoltage(d)
    Temperature = TEMP.getTemperature(voltage)
    print(Temperature)
