import __init__ as I

#===Constants===#
ForceThreshold = .1

#===ADC=Channels===#
PressureChannel = 0
CO2TempChannel = 1
PipeTempChannel = 2

#===BCM=Channels===#
OutputEnable = 22
SolenoidPin = 23
DT = 5
SCK = 6

#===Instantiating=Sensors===#
I.OutputEnable(OutputEnable)
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
COUNTDOWN = range(0,61)

#===Beginning=the=Experiment===#
try:
    print("First, define the nozzle's geometry. This should be one of these:\nN \nU4 \nU3 \nU2 \nU1 \nO \nO1 \nO2 \nO3 \nO4")
    NozzleGeometry = input('Nozzle geometry\n >>>  ')
    print("Now, define the trial number for that geometry\n >>>  ")
    trial = input('Trial number\n >>>  ')
    
    print('This is the start of the solenoid valve test. The valve should open for 1 second and then close for another second.')
    I.time.sleep(1)
    start = 0
    while start != 1:
        Solenoid.SolenoidOPEN()
        I.time.sleep(1)
        Solenoid.SolenoidCLOSE()
        I.time.sleep(1)
        start = int(input('If the test was successful, then press 1 to continue.\n >>>  '))

    Solenoid.SolenoidCLOSE()
    
    start = 0
    while start != 1:
        InitialCO2Mass = float(input('Input the initial mass of the CO2 (g):\n >>>  '))
        start = int(input('Press 1 to continue.\n >>>  '))
    
    start = 0
    while start != 1:
        start = int(input('Insert CO2, then press 1 to continue.\n >>>  '))

    PressureSensor.Calibrate()
    
    
    ForceSensor.CalibrateHX711()
    ForceSensor.reset()
    ForceSensor.tare(20)

    start = 0
    while start != 1:
        testforce = round(ForceSensor.get_weight(1), 2)
        testpressure = round(PressureSensor.getPressure(), 2)
        testtempco2 = round(CO2TempSensor.getTemperature(), 2)
        testtemppipe = round(PipeTempSensor.getTemperature(), 2)
        print('\n\nForce: {}N\nCO2 Temp {}C\nPipe Temp {}C\nPressure {}psi\n'.format(testforce, testtempco2, testtemppipe, round(testpressure / 6894.757,1)))
        start = int(input('If all sensors are functioning correctly, press 1 to continue.\n >>>'))
    print('Starting in...')
    for i in COUNTDOWN:
        print(COUNTDOWN[len(COUNTDOWN)-i-1])
        I.time.sleep(1)
    ForceSensor.reset()
    ForceSensor.tare(20)
    ForceTester = 200
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
        
    Solenoid.SolenoidCLOSE()
    
    file = open('../Data/ExperimentalData/{}_trial_{}.txt'.format(NozzleGeometry, trial), 'w')
    for n in range(len(PressureData)):
        file.write(str(TimeData[n]) + ',' + str(ForceData[n]) + ',' + str(PressureData[n]) + ',' + str(CO2TempData[n]) + ',' + str(PipeTempData[n]) + '\n')
    file.close()

    I.time.sleep(5)
    start = 0
    while start != 1:
        FinalCO2Mass = float(input('Input the final mass of the CO2 (g):\n >>>  '))
        start = int(input('Press 1 to continue.\n >>>  '))

    ChangeInMass = InitialCO2Mass - FinalCO2Mass
    PressureSlope = PressureSensor.CalibrationSlope
    PressureIntercept = PressureSensor.CalibrationIntercept
    ForceReferenceUnit = ForceSensor.REFERENCE_UNIT

    file = open('../Data/ExperimentalData/{}_trial_{}CalibrationValues.txt'.format(NozzleGeometry, trial), 'w')
    file.write('Nozzle Geometry: {}, trial: {}'.format(NozzleGeometry, trial) + '\n' + 'CO2 Initial Mass: {}kg'.format(InitialCO2Mass/1000) + '\n' + 'CO2 Final Mass: {}kg'.format(FinalCO2Mass/1000) + '\n' + 'Change in CO2 mass: {}'.format(ChangeInMass/1000) + '\n' + 'Pressure Calibration Slope: {}'.format(PressureSlope) + '\n' + 'Pressure Calibration Intercept: {}'.format(PressureIntercept) + '\n' + 'Force Reference Unit: {}'.format(ForceReferenceUnit))
    file.close()
    print('Geometry {}, trial {} completed.'.format(NozzleGeometry, trial))
except KeyboardInterrupt:
    print('great job... you made toast')

finally:
    I.RGPIO.cleanup()
    
