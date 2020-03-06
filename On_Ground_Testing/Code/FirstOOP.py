
import RPi.GPIO as GPIO
import time
import numpy as np
from GPIOTranslator import GPIODictionary as GD

GPIO.setmode(GPIO.BOARD)

OUT = GPIO.OUT
IN = GPIO.IN

"""
class MCP3008:

     GPIO.setup(CS, OUT)
     GPIO.setup(CLK, OUT)
     GPIO.setup(DOUT, IN)
     GPIO.setup(DIN, OUT)

     def __init__(self, C, CS, CLK, DOUT, DIN):
     self.C = C
     self.CS = CS
     self.CLK = CLK
     self.DOUT = DOUT
     self.DIN = DIN
"""
C = 0
CS = GD['GPIO12']
CLK = GD['GPIO16']
DOUT = GD['GPIO21']
DIN = GD['GPIO20']

GPIO.setup(CS, OUT)
GPIO.setup(CLK, OUT)
GPIO.setup(DOUT, IN)
GPIO.setup(DIN, OUT)


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
    volts = round(volts, 3)
    return volts

try:
     while True:
          voltage = calc_voltsMCP(readMCP(C, CS, CLK, DOUT, DIN))
          print(voltage)
          time.sleep(.1)
