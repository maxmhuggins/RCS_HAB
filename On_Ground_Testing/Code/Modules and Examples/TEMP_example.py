import __init__ as I

ADCChannel = 1

TemperatureSensor = I.TEMP.TemperatureTransducer(ADCChannel)

while True:

    Temperature = TemperatureSensor.getTemperature()
    print(Temperature)
