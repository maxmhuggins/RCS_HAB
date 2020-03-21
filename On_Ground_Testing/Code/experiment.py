import __init__ as I

#===Constants===#
ForceThreshold = 2

#===ADC=Channels===#
PressureChannel = 0
CO2TempChannel = 1
PipeTempChannel = 2

#===BCM=Channels===#
OutputEnable = 26
SolenoidPin = 18
DT = 20
SCK = 21

#===Instantiating=Sensors===#
Solenoid = I.SND.Solenoid(SolenoidPin)
PressureSensor = I.PR.PressureTransducer(PressureChannel)
ForceSensor = I.HX(DT, SCK)
CO2TempSensor = I.TEMP.TemperatureTransducer(CO2TempChannel)
PipeTempSensor = I.TEMP.TemperatureTransducer(PipeTempChannel)

#===Initializing=Data=Lists===#
TimeData = []
ForceData = []
PressureData = []
CO2TempData = []
PipeTempData = []

#===Beginning=the=Experiment===#
try:
    print("First, define the nozzle's geometry. This should be one of these:\nN \nU4 \nU3 \nU2 \nU1 \nO \nO1 \O2 \O3 \O4")
    NozzleGeometry = input('Nozzle geometry\n >>> ')
    print("Now, define the trial number for that geometry\n >>> ")
    trial = input('Trial number\n >>> ')
    
    print('This is the start of the solenoid valve test. The valve should open for 1 second and then close for another second.')
    I.time.sleep(1)
    start = 0
    while start != 1:
        Solenoid.SolenoidOPEN()
        I.time.sleep(1)
        Solenoid.SolenoidCLOSE()
        I.time.sleep(1)
        start = int(input('If the test was successful, then press 1 to continue.\n >>>'))

    Solenoid.SolenoidCLOSE()

    start = 0
    while start != 1:
        start = int(input('Insert CO2, then press 1 to continue.\n >>>'))

    PressureSensor.Calibrate()
    ForceSensor.CalibrateHX711()
    ForceSensor.reset()
    ForceSensor.tare(200)

    start = 0
    while start != 1:
        testforce = round(ForceSensor.get_weight(1), 2)
        testpressure = round(PressureSensor.getPressure(), 2)
        testtempco2 = round(CO2TempSensor.getTemperature(), 2)
        testtemppipe = round(PipeTempSensor.getTemperature(), 2)
        print('Force: {}\nCO2 Temp {}\nPipe Temp {}\nPressure {}\n\n'.format(testforce, testtempco2, testtemppipe, testpressure))
        start = int(input('If all sensors are functioning correctly, press 1 to continue.\n >>>'))
        
    ForceSensor.reset()
    ForceSensor.tare(200)
    ForceTester = 100
    StartTime = I.time.time()
    while ForceTester >= 0:
        Solenoid.SolenoidOPEN()
        TimeData.append(I.time.time() - StartTime)
        ForceDataPoint = ForceSensor.get_weight(1)
        ForceData.append(ForceDataPoint)
        PressureData.append(PressureSensor.getPressure())
        CO2TempData.append(CO2TempSensor.getTemperature())
        PipeTempData.append(PipeTempSensor.getTemperature())

        if ForceDataPoint < ForceThreshold:
            ForceTester = ForceTester - 1
        else:
            pass

    file = open('../Data/ExperimentalData/{}_trial_{}.txt'.format(NozzleGeometry, trial), 'w')
        for n in range(len(PressureData)):
            file.write(str(TimeData[n]) + ',' + str(ForceData[n]) + ',' + str(PressureData[n]) + ',' + str(CO2TempData[n]) + ',' + str(PipeTempData[n])'\n')
    file.close()
except KeyboardInterrupt:
    print('great job... you made toast')

finally:
    I.RGPIO.cleanup()
    print('Isaac cleaned the oven...')
