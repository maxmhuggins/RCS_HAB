import RPi.GPIO as RGPIO
import time
import numpy as np
from GPIOTranslator import GPIODictionary as GD
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008 as MCP
#============================================================================#

#============================================================================#
C = 0
CS = 12 #Pin 10 on MCP3008
CLK = 16 #Pin 13 on MCP3008
MOSI = 20 #Pin 12 on MCP3008
MISO = 21 #Pin 11 on MCP3008
OE = 26

RGPIO.setmode(GPIO.BCM)
RGPIO.setup(OE, GPIO.OUT)
RGPIO.output(OE, True)

mcp = MCP.MCP3008(clk=CLK, cs=CS, miso=MISO, mosi=MOSI)
#============================================================================#
ref = 5.12
def calc_volts(d, AoM, ref):
    d_int = int(d,2)
    if AoM == 'ADC':
        volts = ref*d_int / 256
        volts = round(volts, 2)
    if AoM == 'MCP':
        volts = ref*d_int / 1024
        volts = round(volts, 2)
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

while True:
    d =  mcp.read_adc(0)
    voltage = calc_volts(d, 'MCP', ref)
    pressure = calc_pressure(voltage)
    print(pressure)
    time.sleep(0.5)
