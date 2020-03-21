import __init__ as I
import numpy as np

class PressureTransducer(I.ADC.MCP3008):
    
    def __init__(self, ADCChannel):
        super().__init__(self)
        self.ADCChannel = ADCChannel
        self.CalibrationSlope = .004119548872180451
        self.CalibrationIntercept = .4595037593984965
        self.ask = 0
        self.del_t = 0
        self.set_reg = 0
        self.ModeVoltages = []
        self.CalibrationVoltages = []
        self.CalibrationPressures = range(40,501,20)

                

    def mode(self, axis=0):
        CalibrationArray = np.array(self.CalibrationVoltages)
        UniquePressures = np.unique(np.ravel(CalibrationArray))       
        testshape = list(CalibrationArray.shape)
        testshape[axis] = 1
        oldmostfreq = np.zeros(testshape)
        oldcounts = np.zeros(testshape)

        for UniquePressure in UniquePressures:
            template = (CalibrationArray == UniquePressure)
            counts = np.expand_dims(np.sum(template, axis),axis)
            mostfrequent = np.where(counts > oldcounts, UniquePressure, oldmostfreq)
            oldcounts = np.maximum(counts, oldcounts)
            oldmostfreq = mostfrequent

        return mostfrequent

    def Calibrate(self):

        while self.ask != 1:
            self.ask = int(input('Are you ready? (1/0)'))
            
        for i in self.CalibrationPressures:
            self.set_reg = 0
            while self.set_reg != '1':
                self.set_reg = input('Is regulator set to {}?'.format(i))
            
            self.CalibrationVoltages = []
            self.del_t = 0
            start_time = I.time.time()
            while self.del_t <= 1:
                voltage = self.getVoltage(self.ADCChannel)
                self.CalibrationVoltages.append(voltage)
                self.del_t = I.time.time() - start_time
                #I.time.sleep(.3)
            
            self.ModeVoltages.append(self.mode())

        x = self.CalibrationPressures
        y = np.array(self.ModeVoltages)
        A = np.vstack([x, np.ones(len(x))]).T
        m, b = np.linalg.lstsq(A, y, rcond=-1.)[0]
        print('Your new calibration slope is', float(m))
        self.CalibrationSlope = float(m)
        self.CalibrationIntercept = float(b)
        print('Your pressure transducer has been succefully calibrated.')

    def getPressure(self):
        p = (self.getVoltage(self.ADCChannel) - self.CalibrationIntercept) / self.CalibrationSlope
        return p
