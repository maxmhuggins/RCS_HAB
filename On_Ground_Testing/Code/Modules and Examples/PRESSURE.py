import __init__ as I

class PressureTransducer(I.ADC.MCP3008):
    ask = 0
    def __init__(self, ADCChannel):
        super().__init__(self)
        self.ADCChannel = ADCChannel
        self.CalibrationSlope = .004119548872180451
        self.CalibrationIntercept = .4595037593984965
        self.del_t = 0
        self.set_reg = 0
        self.CalibrationPressures = range(40,501,20)
        self.ModeVoltages = []
        self.CalibrationVoltages = []

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

        while PressureTransducer.ask != 1:
            self.ask = int(input('Are you ready? (1/0)'))
        
        for i in self.CalibrationPressures:
            while self.set_reg != '1':
                self.set_reg = input('Is regulator set to ', i, '?')

            start_time = time.time()
            while del_t < 100:
                level = mcp.read_adc(self.ADCChannel)
                voltage = ADC.getVoltage(level)
                self.CalibrationVoltages.append(voltage)
                del_t = time.time() - start_time
                time.sleep(.3)
            modes = mode(np.array(self.CalibrationVoltages))
            self.ModeVoltages.append(modes)

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
