import __init__ as I

NumberOfReadings = 3
ReferenceUnit = 136881.76832391287

OE = 22
DT = 5
SCK = 6

I.OutputEnable(OE)

HX = I.HX(DT, SCK)

#Reference Unit can be set manually:
HX.set_reference_unit(ReferenceUnit)

#Or it can be set through a calibration
#HX.CalibrateHX711()
I.time.sleep(10)
HX.reset()
HX.tare(200)

while True:

    Force = HX.get_weight(NumberOfReadings)
    print('Force:    ', Force)
    print('Weight:   ', Force * 1000 / 9.8)
    I.time.sleep(.7)
