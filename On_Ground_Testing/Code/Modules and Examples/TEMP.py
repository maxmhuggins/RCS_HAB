import __init__ as I

class TemperatureTransducer(I.ADC.MCP3008):
    
    def __init__(self, ADCChannel):
        super().__init__(self)
        self.ADCChannel = ADCChannel

    def getTemperature(self): #I don't think this is going to work because the object that gets instantiated given some ADCChannel is never updated for the object. It might though, idk.
        T = (self.getVoltage(self.ADCChannel) - 1.25) / 0.005
        return T
