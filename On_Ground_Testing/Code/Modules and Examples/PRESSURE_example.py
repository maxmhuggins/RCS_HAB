import __init__ as I

ADCChannel = 0
OE = 26

I.OutputEnable(OE)

PressureSensor = I.PR.PressureTransducer(ADCChannel)

while True:

    Pressure = PressureSensor.getPressure()
    print(Pressure)        
    I.time.sleep(.2)
