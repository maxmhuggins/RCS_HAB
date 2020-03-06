import RPi.GPIO as GPIO
import time
import numpy as np
import sys
from hx711 import HX711
from GPIOTranslator import GPIODictionary as GD

voltage_at_vac = .4595037593984965
cal_slope = .004119548872180451
referenceUnit = 2152
V_ref = 3.3

GPIO.setmode(GPIO.BOARD)

OUT = GPIO.OUT
IN = GPIO.IN

C = 0
CS = GD['GPIO12']
CLK = GD['GPIO16']
DOUT = GD['GPIO21']
DIN = GD['GPIO20']

OE = GD['GPIO26']

GPIO.setup(OE, OUT)
GPIO.setup(CS, OUT)
GPIO.setup(CLK, OUT)
GPIO.setup(DOUT, IN)
GPIO.setup(DIN, OUT)

hx = HX711(5, 6)

hx.set_reading_format("MSB", "MSB")

hx.set_reference_unit(referenceUnit)

def readMCP(C, CS, CLK, DOUT, DIN):
     d = ''
     #These next few lines start communication with our friends at channel 1
     GPIO.output(CS, False)
     GPIO.output(DIN, True)
     GPIO.output(CLK, False)
     GPIO.output(CLK, True)
     GPIO.output(CLK, False)
     #######################
     #Input bit selections
     #Sengle ended(not differential)
     #For channel 0 see pg 19 in data sheet
     if C == 0:
          din_control = '1000'
     if C == 1:
          din_control = '1001'
     if C == 2:
          din_control = '1010'
     if C == 3:
          din_control = '1011'
     if C == 4:
          din_control = '1100'
     if C == 5:
          din_control = '1101'
     if C == 6:
          din_control = '1110'
     if C == 7:
          din_control = '1111'
     for n in din_control:
          if n == '1':
               GPIO.output(DIN, True)
          else:
               GPIO.output(DIN, False)
           ###########################
          GPIO.output(CLK, False)
          GPIO.output(CLK, True)
          GPIO.output(CLK, False)
           ###########################
     GPIO.output(CLK, False)
     GPIO.output(CLK, True)
     GPIO.output(CLK, False)
       ##########################
       #This reads in the data synced to the clock pulses
     for n in range(0,10):
          GPIO.output(CLK, False)
          GPIO.output(CLK, True)
          GPIO.output(CLK, False)
           #Listen to the DOUT pin
          DOUT_state = GPIO.input(DOUT)
          if DOUT_state == True:
               d = d + '1'
          else:
               d = d + '0'
       #Finish talking to MCP
     GPIO.output(CS, True)
     GPIO.output(DIN, False)
     return d


def calc_voltsMCP(d):
      d_int = int(d,2)
      volts = V_ref*d_int / 1023
      volts = round(volts, 7)
      return volts

ref = 5
def calc_pressure(voltage, ref): 
     multiplier = 1000 / ref #psi per volt
     p = (voltage - voltage_at_vac) / cal_slope
     return p
 
try:
     hx.reset()
     hx.tare()
     print("Tare done! Add weight now...")
     GPIO.output(OE, True)
     while True:
          print('Mass', round(hx.get_weight(5), 3)
          voltage = calc_voltsMCP(readMCP(0, CS, CLK, DOUT, DIN))
          print('Pressure', calc_pressure(voltage,ref))
          time.sleep(.1)


except KeyboardInterrupt:
     print('great job... you made toast')


finally:
     GPIO.cleanup()
     print('Isaac cleaned the oven.')
