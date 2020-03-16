import numpy as np
import ADC
import SPI
import time
import RPi.GPIO as RGPIO
from GPIOTranslator import GPIODictionary as GD
#=====================================================#
"""                                                   
This section is only here to enable the output enable 
(OE) pin on a level shifter.                          
"""                                                   

OE = GD['GPIO26']

RGPIO.setmode(RGPIO.BOARD)
RGPIO.setup(OE, RGPIO.OUT)
RGPIO.output(OE, True)
#=====================================================#
"""
This is simply setting up the SPI hardware for the 
ADC I am using.
"""
SPI_PORT   = 0
SPI_DEVICE = 0
mcp = ADC.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))
ADC.ReferenceVoltage = 5.12
#=====================================================#

def mode(a, axis=0):
    scores = np.unique(np.ravel(a))       # get ALL unique values
    testshape = list(a.shape)
    testshape[axis] = 1
    oldmostfreq = np.zeros(testshape)
    oldcounts = np.zeros(testshape)

    for score in scores:
        template = (a == score)
        counts = np.expand_dims(np.sum(template, axis),axis)
        mostfrequent = np.where(counts > oldcounts, score, oldmostfreq)
        oldcounts = np.maximum(counts, oldcounts)
        oldmostfreq = mostfrequent

    return mostfrequent

def getPressure(voltage):
    p = (voltage - PressureTransducer.CalibrationIntercept) / PressureTransducer.CalibrationSlope
    return p

class PressureTransducer:

    CalibrationSlope = .004119548872180451
    CalibrationIntercept = .4595037593984965

    @classmethod
    def Calibrate(cls, ADCChannel):
        ask = 0
        CalibrationPressures = range(40,501,20)

        while ask != '1':
            ask = input('Are you ready? (1/0)')
        ModeVoltages = []
        for i in CalibrationPressures:
            del_t = 0
            set_reg = 0
            CalibrationVoltages = []

            while set_reg != '1':
                print('Is regulator set to ', i, '?')
                set_reg = input()

            start_time = time.time()
            while del_t < 100:
                level = mcp.read_adc(ADCChannel)
                voltage = ADC.getVoltage(level)
                CalibrationVoltages.append(voltage)
                del_t = time.time() - start_time
                time.sleep(.3)
            modes = mode(np.array(CalibrationVoltages))
            ModeVoltages.append(modes)

        x = CalibrationPressures
        y = np.array(ModeVoltages)
        A = np.vstack([x, np.ones(len(x))]).T
        m, b = np.linalg.lstsq(A, y, rcond=-1.)[0]
        print('Your new calibration slope is', float(m))
        cls.CalibrationSlope = float(m)
        cls.CalibrationIntercept = float(b)
        print('Your pressure transducer has been succefully calibrated.')
