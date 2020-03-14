import numpy as np

def getPressure(voltage):
     p = (voltage - PressureTransducer.CalibrationIntercept) / PressureTransducer.CalibrationSlope
     return p

class PressureTransducer:

     CalibrationSlope = .004119548872180451
     CalibrationIntercept = .4595037593984965

     @classmethod
     def Calibrate(cls, CalibrationPressures, CalibrationVoltages):
          x = CalibrationPressures
          y = np.array(CalibrationVoltages)
          A = np.vstack([x, np.ones(len(x))]).T
          m, b = np.linalg.lstsq(A, y, rcond=-1.)[0]
          print('Your new calibration slope is', m)
          cls.CalibrationSlope = m
          cls.CalibrationIntercept = b
          print('Your pressure transducer has been succefully calibrated.')
