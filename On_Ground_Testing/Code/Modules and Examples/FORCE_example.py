from FORCE import HX711
from GPIOTranslator import GPIODictionary as GD
#============================================================================#
hx = HX711(GD['GPIO5'], GD['GPIO6'])
hx.set_reading_format("MSB", "MSB")


#Reference Unit can be set manually:

#referenceUnit = 954.5
#hx.set_reference_unit(referenceUnit)


hx.reset()

hx.tare()

#Or it can be set through a calibration
hx.CalibrateHX711()

while True:
    Force = hx.get_weight(3)
    print(Force)
