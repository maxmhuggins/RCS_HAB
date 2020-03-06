import RPi.GPIO as GPIO
import time
import numpy as np

GPIO.setmode(GPIO.BOARD)

C = 0
CS = 32
CLK = 36
DOUT = 40
DIN = 38

GPIO.setup(CS, GPIO.OUT)
GPIO.setup(CLK, GPIO.OUT)
GPIO.setup(DOUT, GPIO.IN)
GPIO.setup(DIN, GPIO.OUT)

#============================================================================#

def readADC():
    #set initial binary to as empty
    d = ''
    GPIO.output(CS,False)
    #oneclock pulse
    #set CLK low
    GPIO.output(CLK,False)
    #Set clk high
    GPIO.output(CLK,True)
    GPIO.output(CLK,False)
    #end CLK pulse
    #now to read data synced to more clokc pulses
    for n in range(0,8): #read in 8 bits, 0-7
        #one clock pulse
        #set CLK low then high
        GPIO.output(CLK,False)
        GPIO.output(CLK,True)
        GPIO.output(CLK,False)
        DO_state = GPIO.input(DO)
        if DO_state == True:
            d = d+'1'
        else:
            d = d + '0'
        #Do until all bits are read
    #End convo w/ ADC
    GPIO.output(CS,True)
    #Return binary
    return d

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
        volts = round(volts, 3)
    return volts
                    
#============================================================================#

V_0 = .5
T_c = .01
R1 = 9840

def calc_temp(ref,volts,sensor):
    if sensor == 'LM34':
        temp = volts / .01
        temp = (temp-32)*(5/9)
    elif sensor == 'BudgetLM34':
        temp = (np.abs(volts - V_0)) / T_c
    elif sensor == 'Thermistor':
        Resistor_value = (volts * R1)/(ref - volts)   
        temp = (1 /(
                    1.506*10**(-3) +
                    1.615*10**(-4) * np.log(Resistor_value)+
                    4.242*10**(-7) * (np.log(Resistor_value))**3)
                ) - 273
    temp = round(temp,2)
    return temp

#============================================================================#

def calc_resist_Photoresist(ref,volts):
    Resistor_value = (volts * R1)/(ref - volts)
    if Resistor_value < 15000:
        return Resistor_value

#============================================================================#
