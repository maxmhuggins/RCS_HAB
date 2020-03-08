import numpy as np
from scipy import stats

class PressureTransducer:
     ReferenceVoltage = 5
     CalibrationSlope = 0
     CalibrationIntercept = 0
     def __init__(self, voltage):
          self.voltage = voltage
     def getPressure(self):
          p = (self.voltage - PressureTransducer.CalibrationIntercept) / PressureTransducer.CalibrationSlope
          return p

     @classmethod
     def Calibrate(cls, CalibrationPressures, CalibrationVoltages):
          x = np.array(self.CalibrationPressures)
          y = np.array(self.CalibrationVoltages)
          m, b, r_value, p_value, std_err = stats.linregress(x,y)
          print('Your new calibration slope is', m)
          cls.CalibrationSlope = m
          cls.CalibrationIntercept = b
          print('Your pressure transducer has been succefully calibrated.')
