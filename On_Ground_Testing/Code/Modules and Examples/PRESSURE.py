import time

class PressureTransducer:
    
    def __init__(self, ADCChannel)
        import ADC
        import SPI
        import numpy as np
        self.ADCChannel = ADCChannel
        self._device = ADC.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))
        self.voltage = self._device.getVoltage(self._device.read_adc(self.ADCChannel)))
        self.CalibrationSlope = .004119548872180451
        self.CalibrationIntercept = .4595037593984965
        self.ADCChannel = ADCChannel
        self.CalibrationVoltages = []
        self.del_t = 0
        self.set_reg = 0
        self.ask = 0
        self.CalibrationPressures = range(40,501,20)

    def mode(self, axis=0):
        UniquePressures = np.unique(np.ravel(self.CalibrationVoltages))       
        testshape = list(self.CalibrationVoltages.shape)
        testshape[axis] = 1
        oldmostfreq = np.zeros(testshape)
        oldcounts = np.zeros(testshape)

        for UniquePressure in UniquePressures:
            template = (a == UniquePressure)
            counts = np.expand_dims(np.sum(template, axis),axis)
            mostfrequent = np.where(counts > oldcounts, UniquePressure, oldmostfreq)
            oldcounts = np.maximum(counts, oldcounts)
            oldmostfreq = mostfrequent

        return mostfrequent

    def Calibrate(self):
        
        while ask != '1':
            ask = input('Are you ready? (1/0)')
        ModeVoltages = []
        for i in self.CalibrationPressures:
            while self.set_reg != '1':
                print('Is regulator set to ', i, '?')
                self.set_reg = input()

            start_time = time.time()
            while del_t < 100:
                level = mcp.read_adc(self.ADCChannel)
                voltage = ADC.getVoltage(level)
                self.CalibrationVoltages.append(voltage)
                del_t = time.time() - start_time
                time.sleep(.3)
            modes = mode(np.array(self.CalibrationVoltages))
            ModeVoltages.append(modes)

        x = self.CalibrationPressures
        y = np.array(ModeVoltages)
        A = np.vstack([x, np.ones(len(x))]).T
        m, b = np.linalg.lstsq(A, y, rcond=-1.)[0]
        print('Your new calibration slope is', float(m))
        self.CalibrationSlope = float(m)
        self.CalibrationIntercept = float(b)
        print('Your pressure transducer has been succefully calibrated.')

    def getPressure(self):
        p = (self.voltage - self.CalibrationIntercept) / self.CalibrationSlope
        return p
