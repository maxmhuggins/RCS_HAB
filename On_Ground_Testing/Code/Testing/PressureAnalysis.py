"""
First: Determine a standard value by taking many data samples at very slow sample rate and determine mean, median, mode, range, and std. dev. for it.

Second: Run many different sample rates determining the mean, median, mode, range, and std. dev. for each of them.

Third: Determine the sample rate that minimizes the difference between the standard and the tested sample rate. 
        Maybe sum the differences and whichever sum is the smallest is the best
        option. Or weight them with some multiplier.
"""
#============================================================================#
import time
import SPI
import RPi.GPIO as RGPIO
import numpy as np
import mcp3008 as MCP
import matplotlib.pyplot as plt
import PRESSURE as PR
#============================================================================#
OE = 26

RGPIO.setmode(RGPIO.BCM)
RGPIO.setup(OE, RGPIO.OUT)
RGPIO.output(OE, True)

SPI_PORT   = 0
SPI_DEVICE = 0
mcp = MCP.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))
MCP.ReferenceVoltage = 5.12
#============================================================================#
PR.CalibrationSlope = .004119548872180451
PR.CalibrationIntercept = .4595037593984965
#============================================================================#
SampleSize = 500
StandardPressures = []
StandardTimes = []
PressureData = []
TimeData = []
SleepTimes = np.linspace(0.01,.1,10)
SampleRateStats = []
#============================================================================#
def DetermineMean(PressureData):
    average = np.average(PressureData)
    return average

def DetermineMedian(PressureData):
    median = np.median(PressureData)
    return median
    
def DetermineMode(PressureData):
    mode = np.mode(PressureData)
    return mode
 
def DetermineRange(PressureData):
    arange = np.arange(PressureData)
    return arange

def DetermineStdDev(PressureData):
    stddev = np.std(PressureData)
    return stddev

def DifferencesInStats(StandardStats, SampleRateStats):
    summer = 0
    for i in range(0,len(StandardStats)):
        summer = summer + abs(StandardStats[i] - SampleRateStats[i])
    return summer
#============================================================================#
try:
    #========================================================================#
    Points = 0
    StartTime = time.time()
    while Points <= SampleSize:
        ChangeInTime = time.time() - StartTime
        d = mcp.read_adc(0)
        voltage = MCP.CalculateVoltage(d)
        PressurePoint = PR.getPressure(voltage)
        StandardPressures.append(PressurePoint)
        StandardTimes.append(ChangeInTime)
        Points = Points + 1
        time.sleep(1)

    StandardPressures = np.array(StandardPressures)
    StandardMean = DetermineAverage(StandardPressures)
    StandardMedian = DetermineMedian(StandardPressures)
    StandardMode = DetermineMode(StandardPressures)
    StandardRange = DetermineRange(StandardPressures)
    StandardStdDev = DetermineStdDev(StandardPressures)

    print('Statistics for the standard are:\nMean: {}\nMedian: {}\nMode: {}\nRange: {}\nStandard Deviation: {}'.format(round(StandardMean, 3), round(StandardMedian, 3), round(StandardMode, 3), round(StandardRange, 3), round(StandardStdDev, 3))
    
    file = open('../../Data/PressureAnalysis/PressureTestingStandard.txt', 'w')
    file.write('Statistics for the standard are:\nMean: {}\nMedian: {}\nMode: {}\nRange: {}\nStandard Deviation: {}'.format(round(StandardMean, 3), round(StandardMedian, 3), round(StandardMode, 3), round(StandardRange, 3), round(StandardStdDev, 3))
    file.close()    

    StandardStats = [StandardAverage, StandardMedian, StandardMode, StandardRange, StandardStdDev]
    #========================================================================#
#============================================================================#
    #========================================================================#
    for i in SleepTimes:
        Points = 0
        SampleRateStats = []
        StartTime = time.time()
        while Points <= SampleSize:
            ChangeInTime = time.time() - StartTime
            d = mcp.read_adc(0)
            voltage = MCP.CalculateVoltage(d)
            PressurePoint = PR.getPressure(voltage)
            PressureData.append(PressurePoint)
            TimeData.append(ChangeInTime)
            Points = Points + 1
            time.sleep(i)

        plt.plot(TimeData, PressureData, linewidth=1, label='Delay of {}s, length of {}'.format(round(i, 2), len(TimeData)))
        plt.legend(loc='best', fontsize=5)
        plt.ylim(20,30)
        plt.savefig('../../Data/PressureAnalysis/SleepTimeOf {}s.png'.format(round(i, 3)))
        plt.close()

        RatePressures = np.array(PressureData)

        RateMean = DetermineAverage(PressureData)
        RateMedian = DetermineMedian(PressureData)
        RateMode = DetermineMode(PressureData)
        RateRange = DetermineRange(PressureData)
        RateStdDev = DetermineStdDev(PressureData)

        print('Statistics for a sleep time of {}s are:\nMean: {}\nMedian: {}\nMode: {}\nRange: {}'.format(round(i,3), round(RateMean, 3), round(RateMedian, 3), round(RateMode, 3), round(RateRange, 3))

        SampleRateStats.append(RateMean, RateMedian, RateMode, RateRange, RateStdDev)
        
        Difference = DifferencesInStats(StandardStats, SampleRateStats)
        print('The difference in stats for the standard and a sleep time of {}s is {}'.format(round(i,3), Difference)

        file = open('../../Data/PressureAnalysis/PressureTestingSleepOf{}.txt'.format(round(i, 3)), 'w')
        for n in range(len(PressureData)):
            file.write(str(TimeData[n]) + ',' + str(PressureData[n]) + '\n')
        file.close()

        file = open('../../Data/PressureAnalysis/PressureTestingStatsSleepOf{}.txt'.format(round(i,3)), 'w')
        file.write('Statistics for a sleep time of {}s are:\nMean: {}\nMedian: {}\nMode: {}\nRange: {}\nStandard Deviation: {}'.format(round(i,3), round(RateMean, 3), round(RateMedian, 3), round(RateMode, 3), round(RateRange, 3), round(RateStdDev, 3))
        file.close()

        time.sleep(.1)
    #========================================================================#
except KeyboardInterrupt:
    print('great job... you made toast')

finally:
    RGPIO.cleanup()
    print('Isaac cleaned the oven...')

