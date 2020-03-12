import RPi.GPIO as RGPIO
import time
import numpy as np
from GPIOTranslator import GPIODictionary as GD
import SPI
import mcp3008 as MCP
#============================================================================#

#============================================================================#
##C = 0
##CS = 12 #Pin 10 on MCP3008
##CLK = 16 #Pin 13 on MCP3008
##MOSI = 20 #Pin 12 on MCP3008
##MISO = 21 #Pin 11 on MCP3008
OE = 26

RGPIO.setmode(RGPIO.BCM)
RGPIO.setup(OE, RGPIO.OUT)
RGPIO.output(OE, True)

SPI_PORT   = 0
SPI_DEVICE = 0
mcp = MCP.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))
#mcp = MCP.MCP3008(clk=CLK, cs=CS, miso=MISO, mosi=MOSI)
#============================================================================#
ref = 5.12
def calc_volts(d_int):
    volts = ref*d_int / 1023
    return volts

#============================================================================#
voltage_at_vac = .4595037593984965
cal_slope = .004119548872180451

def calc_pressure(voltage): 
    p = (voltage - voltage_at_vac) / cal_slope
    return round(p,4)

#============================================================================#

def calc_temp(voltage):
     T = (voltage - 1.25) / 0.005
     return T
#============================================================================#

try:
    while True:
        d =  mcp.read_adc(0)
        print(d)
        voltage = calc_volts(d)
        pressure = calc_pressure(voltage)
        print(pressure)

except KeyboardInterrupt:
    print('great job... you made toast')

finally:
    RGPIO.cleanup()
    print('Isaac cleaned the oven...')

