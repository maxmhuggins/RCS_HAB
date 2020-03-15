import SPI
import ADC
import TEMP
import time
import PRESSURE as PR
import RPi.GPIO as RGPIO
from GPIOTranslator import GPIODictionary as GD
from FORCE import HX711

OE = GD['GPIO26']
PRESSURECHANNEL = 0
TEMPCHANNEL = 1
SPI_PORT   = 0
SPI_DEVICE = 0
HX = HX711(GD['GPIO20'], GD['GPIO21'])

RGPIO.setmode(RGPIO.BOARD)
RGPIO.setup(OE, RGPIO.OUT)
RGPIO.output(OE, True)

mcp = ADC.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))

HX.set_reading_format("MSB", "MSB")
ADC.ReferenceVoltage = 5.003
"""
PR.PressureTransducer.Calibrate(PRESSURECHANNEL)
HX.CalibrateHX711()
"""
referenceUnit = 954.5
HX.set_reference_unit(referenceUnit)

HX.reset()
HX.tare()
try:
    while True:
        PressureLevel = mcp.read_adc(PRESSURECHANNEL)
        TemperatureLevel = mcp.read_adc(TEMPCHANNEL)
        
        PressureVoltage = ADC.getVoltage(PressureLevel)
        TemperatureVoltage = ADC.getVoltage(TemperatureLevel)
        
        Pressure = PR.getPressure(PressureVoltage)
        Force = HX.get_weight(1)
        Temperature = TEMP.getTemperature(TemperatureVoltage)

        print('Pressure: {}\nForce: {}\nTemperature: {}\n'.format(round(Pressure, 3), round(Force, 3), round(Temperature, 3)))
        HX.reset()
        time.sleep(.1)

except KeyboardInterrupt:
    print('great job... you made toast')

finally:
    RGPIO.cleanup()
    print('Isaac cleaned the oven...')

