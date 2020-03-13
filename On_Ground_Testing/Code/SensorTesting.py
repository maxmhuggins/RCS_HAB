import RPi.GPIO as GPIO
import time
import numpy as np
from GPIOTranslator import GPIODictionary as GD
from hx711 import HX711
#============================================================================#
EMULATE_HX711=False
referenceUnit = 954.5
hx = HX711(GD['GPIO5'], GD['GPIO6'])
hx.set_reading_format("MSB", "MSB")
hx.set_reference_unit(referenceUnit)
#============================================================================#
C = 0
CS = GD['GPIO12'] #Pin 10 on MCP3008
CLK = GD['GPIO16'] #Pin 13 on MCP3008
DOUT = GD['GPIO20'] #Pin 12 on MCP3008
DIN = GD['GPIO21'] #Pin 11 on MCP3008
OE = GD['GPIO26']

GPIO.setmode(GPIO.BOARD)
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
    return round(p,4)

#============================================================================#

def calc_temp(voltage):
     T = (voltage - 1.25) / 0.005
     return T
#============================================================================#
ref = 5.12

#hx.reset()

#hx.tare()

try:
    ChangeInTime = 0
    PressureData = []
    TimeData = []
    StartTime = time.time()
    while ChangeInTime < 30:
        ChangeInTime = time.time() - StartTime
        dig_read_0 = readMCP(0, CS, CLK, DOUT, DIN)
        #dig_read_1 = readMCP(1, CS, CLK, DOUT, DIN)
        voltage_0 = calc_volts(dig_read_0, 'MCP', ref)
        #voltage_1 = calc_volts(dig_read_1, 'MCP', ref)
        pressure = calc_pressure(voltage_0, ref)
        PressureData.append(pressure)
        TimeData.append(ChangeInTime)
        time.sleep(.1)
        #force = hx.get_weight(3)
        #temperature = round(calc_temp(voltage_1), 4)
    file = open('../Data/PressureTesting.txt', 'w')
    for n in range(len(PressureData)):
       #Write the data as comma delimites
        file.write(str(TimeData[n]) + ',' + str(PressureData[n]) + '\n')
        #always close the file you are using
    
    file.close()
        
#        print('Pressure transducer voltage {}V. \n'
#              'Temperature probe voltage {}V \n\n'.format(voltage_0, voltage_1, ))
#        
#        print('Load cell {}g \n'
#              'Pressure transducer {}psi. \n'
#              'Temperature {}C \n\n'.format(force, pressure, temperature))
#        time.sleep(.1)

except KeyboardInterrupt:
    print('great job... you made toast')

finally:
    GPIO.cleanup()
    print('Isaac cleaned the oven...')

