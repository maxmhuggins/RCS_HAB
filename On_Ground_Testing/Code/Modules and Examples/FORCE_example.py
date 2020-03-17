import __init__ as I

NumberOfReadings = 3
ReferenceUnit = 954.5

HX = I.HX(I.GD['GPIO20'], I.GD['GPIO21'])
HX.set_reading_format("MSB", "MSB")

#Reference Unit can be set manually:
HX.set_reference_unit(ReferenceUnit)
#Or it can be set through a calibration
#HX.CalibrateHX711()

HX.reset()
HX.tare(60)

while True:

    Force = HX.get_weight(NumberOfReadings)
    print(Force)
