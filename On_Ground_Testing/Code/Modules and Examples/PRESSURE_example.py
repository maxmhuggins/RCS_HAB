import PRESSURE as PR
import ADC
import SPI
import time
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
"""
This section sets up the SPI hardware for the ADC I
am using.
"""

SPI_PORT   = 0
SPI_DEVICE = 0
mcp = ADC.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))
#=====================================================#

PR.PressureTransducer.Calibrate(0)
while True:
    d = mcp.read_adc(0)
    voltage = ADC.getVoltage(d)
    Pressure = PR.getPressure(voltage)
    print(Pressure)
    time.sleep(.5)
        

