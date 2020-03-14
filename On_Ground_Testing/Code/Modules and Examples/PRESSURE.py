import numpy as np
import ADC
import SPI
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
"""
This is simply setting up the SPI hardware for the 
ADC I am using.
"""
SPI_PORT   = 0
SPI_DEVICE = 0
mcp = ADC.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))
ADC.ReferenceVoltage = 5.12
#=====================================================#

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
 
        for i in CalibrationPressures:
            del_t = 0
            set_reg = 0
            CalibrationVoltages = []

            while set_reg != '1':
                print('Is regulator set to ', i, '?')
                set_reg = input()

            start_time = time.time()
            while del_t < 30:
                level = mcp.read_adc(ADCChannel)
                voltage = ADC.getVoltage(level)
                CalibrationVoltages.append(voltage)
                del_t = time.time() - start_time
                time.sleep(.2)
            mode = np.mode(np.array(CalibrationVoltages))
            ModeVoltages.append(mode)

          x = CalibrationPressures
          y = np.array(ModeVoltages)
          A = np.vstack([x, np.ones(len(x))]).T
          m, b = np.linalg.lstsq(A, y, rcond=-1.)[0]
          print('Your new calibration slope is', m)
          cls.CalibrationSlope = m
          cls.CalibrationIntercept = b
          print('Your pressure transducer has been succefully calibrated.')
