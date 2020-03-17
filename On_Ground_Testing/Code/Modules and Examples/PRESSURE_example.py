import __init__

ADCChannel = 0

PressureSensor = PR.PressureTransducer.Calibrate(ADCChannel)

while True:

    Pressure = PressureSensor.getPressure()
    print(Pressure)
        

