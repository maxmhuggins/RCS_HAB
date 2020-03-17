
class TemperatureTransducer:
    
    def __init__(self, ADCChannel)
        self.ADCChannel = ADCChannel
        self._device = ADC.MCP3008(spi=SPI.SpiDev())
        self.voltage = self._device.getVoltage(self._device.read_adc(self.ADCChannel)))

    def getTemperature(self): #I don't think this is going to work because the object that gets instantiated given some ADCChannel is never updated for the object. It might though, idk.
        T = (self.voltage - 1.25) / 0.005
        return T
