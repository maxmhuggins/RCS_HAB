#=============================================================================#
import PRESSURE
import RPi.GPIO as GPIO
import time
import numpy as np
import ADC
from GPIOTranslator import GPIODictionary as GD
#=============================================================================#
ref = 5 
act_p = range(40,101,20)
avg_volts = []
ask = 0
PressureTransducerChannel = 0

CLK = GD['GPIO16']
CS = GD['GPIO12']
MOSI = GD['GPIO21']
MISO = GD['GPIO20']
OE = GD['GPIO26']

GPIO.setmode(GPIO.BOARD)

GPIO.setup(CLK, GPIO.OUT)
GPIO.setup(CS, GPIO.OUT)
GPIO.setup(MOSI, GPIO.IN)
GPIO.setup(MISO, GPIO.OUT)
GPIO.setup(OE, GPIO.OUT)

GPIO.output(OE, True)

myADC =  ADC.MCP3008(CLK, CS, MOSI, MISO)
#=============================================================================#
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
            voltage = myADC.measure(PressureTransducerChannel)
            measrd_volts.append(voltage)
            time.sleep(.05)
            del_t = time.time() - start_time
        avg = sum(measrd_volts)/len(measrd_volts)
        avg_volts.append(avg)
        print(avg)
    PRESSURE.PressureTransducer.Calibrate(act_p, avg_volts)
#=============================================================================#
    while True:
        voltage = myADC.measure(PressureTransducerChannel)
        PressureMeasurement = PRESSURE.getPressure(voltage)
        print('Pressure is ', PressureMeasurement)
        time.sleep(.1)
#=============================================================================#
except KeyboardInterrupt:
     print('great job... you made toast')

finally:
     GPIO.cleanup()
     print('Isaack cleaned the oven.')
#=============================================================================#
