import __init__ as I

NumberOfReadings = 3
ReferenceUnit = 954.5

OE = 26
DT = 20
SCK = 21

I.OutputEnable(OE)

HX = I.HX(DT, SCK)

#Reference Unit can be set manually:
HX.set_reference_unit(ReferenceUnit)

#Or it can be set through a calibration
#HX.CalibrateHX711()

HX.reset()
HX.tare(200)

while True:

    Force = HX.get_weight(NumberOfReadings)
    print(Force)
