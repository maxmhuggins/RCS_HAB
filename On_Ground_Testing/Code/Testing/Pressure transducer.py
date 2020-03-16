# -*- coding: utf-8 -*-
"""
Created on Tue Jan  7 18:35:25 2020

@author: maxhu
"""
#============================================================================#
import RPi.GPIO as GPIO
import time
import numpy as np
from GPIOTranslator import GPIODictionary as GD
#============================================================================#
GPIO.setmode(GPIO.BOARD)

C = 0
CS = GD['GPIO12'] #Pin 10 on MCP3008
CLK = GD['GPIO16'] #Pin 13 on MCP3008
DOUT = GD['GPIO21'] #Pin 12 on MCP3008
DIN = GD['GPIO20'] #Pin 11 on MCP3008

OE = GD['GPIO26']

PR_TRANS = 11
atm = 14.6959 #psi per atm
GPIO.setup(PR_TRANS, GPIO.IN)

GPIO.setup(CS, GPIO.OUT)
GPIO.setup(CLK, GPIO.OUT)
GPIO.setup(DOUT, GPIO.IN)
GPIO.setup(DIN, GPIO.OUT)
GPIO.setup(OE, GPIO.OUT)

GPIO.output(OE, True)
#============================================================================#
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

#============================================================================#

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

def calc_pressure(voltage, ref): 
    p = (voltage - voltage_at_vac) / cal_slope
    return p

#============================================================================#
ref = 5

try:
    while True:
        dig_read = readMCP(0, CS, CLK, DOUT, DIN)
        voltage = calc_volts(dig_read, 'MCP', ref)
        pressure = calc_pressure(voltage, ref)
        print('pressure', pressure)
        time.sleep(.1)
except KeyboardInterrupt:
    print('great job... you made toast')

finally:
    GPIO.cleanup()
    print('Isaac cleaned the oven...')
