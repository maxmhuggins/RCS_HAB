import __init__

ADCChannel = 1

TemperatureSensor = TEMP.TemperatureTransducer(ADCChannel)

while True:

    Temperature = TemperatureSensor.getTemperature()
    print(Temperature)
