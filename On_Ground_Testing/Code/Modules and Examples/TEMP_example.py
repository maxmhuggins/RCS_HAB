import __init__ as I

ADCChannel_1 = 1
ADCChannel_2 = 2

I.OutputEnable(26)

TemperatureSensor_1 = I.TEMP.TemperatureTransducer(ADCChannel_1)
TemperatureSensor_2 = I.TEMP.TemperatureTransducer(ADCChannel_2)

while True:

    Temperature_1 = TemperatureSensor_1.getTemperature()
    Temperature_2 = TemperatureSensor_2.getTemperature()
    print(Temperature_1, Temperature_2)
