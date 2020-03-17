import __init__

NumberOfReadings = 3
ReferenceUnit = 954.5

HX = HX711(GD['GPIO5'], GD['GPIO6'])
HX.set_reading_format("MSB", "MSB")

#Reference Unit can be set manually:
HX.set_reference_unit(ReferenceUnit)
#Or it can be set through a calibration
HX.CalibrateHX711()

HX.reset()
HX.tare()

while True:

    Force = HX.get_weight(NumberOfReadings)
    print(Force)
