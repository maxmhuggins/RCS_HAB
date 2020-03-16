import PRESSURE as PR
import time
import RPi.GPIO as RGPIO
#=====================================================#
"""                                                   
This section is only here to enable the output enable 
(OE) pin on a level shifter.                          
"""                                                   

OE = 26

RGPIO.setmode(RGPIO.BCM)
RGPIO.setup(OE, RGPIO.OUT)
RGPIO.output(OE, True)
#=====================================================#

PR.PressureTransducer.Calibrate(0)
while True:
    Pressure = PR.getPressure()
    print(Pressure)
    time.sleep(.5)
        

