#=============================================================================#
import PRESSURE
import RPi.GPIO as GPIO
import time
import numpy as np
import ADC
#=============================================================================#
ref = 5 #Measure this and add smoothing caps later
act_p = range(40,501,20) #Use a larger range later
avg_volts = []
ask = 0
PressureTransducerChannel = 0
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
            voltage = ADC.MCP3008.measure(PressureTransducerChannel)
            measrd_volts.append(voltage)
            time.sleep(.05)
            del_t = time.time() - start_time
        avg = sum(measrd_volts)/len(measrd_volts)
        avg_volts.append(avg)
        print(avg)
    PRESSURE.PressureTransducer.Calibrate(act_p, avg_volts)
#=============================================================================#
    while True:
        voltage = ADC.MCP3008.measure(PressureTransducerChannel)
        PressureMeasurement = PRESSURE.PressureTransducer.getPressure(voltage)
        print('Pressure is ', PressureMeasurement)
        time.sleep(.1)
#=============================================================================#
except KeyboardInterrupt:
     print('great job... you made toast')

finally:
     GPIO.cleanup()
     print('Isaac cleaned the oven.')
#=============================================================================#
