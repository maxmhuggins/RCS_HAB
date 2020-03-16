# -*- coding: utf-8 -*-
"""
Created on Tue Jan  7 18:35:25 2020

@author: maxhu
"""
#============================================================================#
import RPi.GPIO as GPIO
import time
import numpy as np
#============================================================================#
GPIO.setmode(GPIO.BOARD)

C = 0
CS = 32 #Pin 10 on MCP3008
CLK = 36 #Pin 13 on MCP3008
DOUT = 40 #Pin 12 on MCP3008
DIN = 38 #Pin 11 on MCP3008

PR_TRANS = 11
atm = 14.6959 #psi per atm
GPIO.setup(PR_TRANS, GPIO.IN)

GPIO.setup(CS, GPIO.OUT)
GPIO.setup(CLK, GPIO.OUT)
GPIO.setup(DOUT, GPIO.IN)
GPIO.setup(DIN, GPIO.OUT)
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

def calc_pressure(voltage, ref): 
    multiplier = 1000 / ref #psi per volt
    p = voltage * multiplier - 100
    p = round(p, 2)
    return p

#============================================================================#
ref = 5 #Measure this and add smoothing caps later
act_p = range(40,501,20) #Use a larger range later
avg_volts = []
ask = 0

#==================#
try:
    #=====================================#
    while ask != '1':
        ask = input('Are you ready? (1/0)')
    #=====================================#   
    for i in act_p:
        del_t = 0
        set_reg = 0
        measrd_volts = []
        #========================================================# 
        while set_reg != '1':
            print('Is regulator set to ', i, '?')
            set_reg = input()
        #========================================================#    
        start_time = time.time()
        while del_t < 10:
            measrd_volts.append(calc_volts(readMCP(0, CS, CLK, DOUT, DIN), 'MCP', ref))
            time.sleep(.05)
            del_t = time.time() - start_time
        avg = sum(measrd_volts)/len(measrd_volts)
        avg_volts.append(avg)
        print(avg)
        #========================================================#
    file = open('calibration_data.txt', 'w')
    for n in range(len(avg_volts)):
        file.write(str(act_p[n]) + ',' + str(round(avg_volts[n],2)) + '\n')
    file.close()
    
#============================================================================#   
except KeyboardInterrupt:
    print('great job... you made toast')

finally:
    GPIO.cleanup()
    print('Isaac cleaned the oven...')
#============================================================================#
#To improve this code:
#   have it wait longer at a given pressure level
#   Use smoothing caps to quiet supply voltage or use regulator
#   Use BNC connector for transducer
#   Measure the reference voltage with meter and change ref value
#   Use a finer guage for pressure
#   Use higher pressure ranges
#   Use higher bit ADC like the 
