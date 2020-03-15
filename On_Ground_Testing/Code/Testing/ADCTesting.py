import RPi.GPIO as RGPIO
import time
import numpy as np
from GPIOTranslator import GPIODictionary as GD
import SPI
import mcp3008 as MCP
import matplotlib.pyplot as plt
#============================================================================#

#============================================================================#
##C = 0
##CS = 12 #Pin 10 on MCP3008
##CLK = 16 #Pin 13 on MCP3008
##MOSI = 20 #Pin 12 on MCP3008
##MISO = 21 #Pin 11 on MCP3008
OE = 26

RGPIO.setmode(RGPIO.BCM)
RGPIO.setup(OE, RGPIO.OUT)
RGPIO.output(OE, True)

SPI_PORT   = 0
SPI_DEVICE = 0
mcp = MCP.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))
#mcp = MCP.MCP3008(clk=CLK, cs=CS, miso=MISO, mosi=MOSI)
#============================================================================#
ref = 5.12
def calc_volts(d_int):
    volts = ref*d_int / 1023
    return volts

#============================================================================#
voltage_at_vac = .4595037593984965
cal_slope = .004119548872180451

def calc_pressure(voltage): 
    p = (voltage - voltage_at_vac) / cal_slope
    return round(p,4)

#============================================================================#

def calc_temp(voltage):
     T = (voltage - 1.25) / 0.005
     return T
#============================================================================#

try:
##    while True:
##        d =  mcp.read_adc(0)
##        voltage = calc_volts(d)
##        pressure = calc_pressure(voltage)
##        print(pressure)
##        time.sleep(0.1)
    SleepTimes = np.linspace(0.01,.1,10)
    for i in SleepTimes:
        ChangeInTime = 0
        PressureData = []
        TimeData = []
        StartTime = time.time()
        while ChangeInTime < 1:
            ChangeInTime = time.time() - StartTime
            PressureData.append(calc_pressure(calc_volts(mcp.read_adc(0))))
            TimeData.append(ChangeInTime)
            time.sleep(i)
        plt.plot(TimeData, PressureData, linewidth=1, label='Delay of {}s, length of {}'.format(round(i, 2), len(TimeData)))
        plt.legend(loc='best', fontsize=5)
        plt.ylim(190,230)
        plt.savefig('../Data/SleepTimeOf {}s.png'.format(round(i, 2)))
        plt.close()
        file = open('../Data/PressureTestingSleepOf{}.txt'.format(round(i, 2)), 'w')
        for n in range(len(PressureData)):
           #Write the data as comma delimites
            file.write(str(TimeData[n]) + ',' + str(PressureData[n]) + '\n')
            #always close the file you are using

        file.close()
##        plt.savefig('../Data/SleepTimes.png')
        print('Time sleep of {}s done.'.format(i))
        time.sleep(.1)

"""
Need to look into Nyquist's thm. Should be able to determine what sample rate is going to be
best given the noise.
"""

except KeyboardInterrupt:
    print('great job... you made toast')

finally:
    RGPIO.cleanup()
    print('Isaac cleaned the oven...')

