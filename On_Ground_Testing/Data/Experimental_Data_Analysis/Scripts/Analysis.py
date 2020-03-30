import numpy as np
import matplotlib.pyplot as plt

AreaRatio = []
Geometries = ['O4', 'O3', 'O2', 'O1', 'O', 'U1', 'U2', 'U3', 'U4', 'N']
r_e = [5, 4, 3, 2, 1.59323, 1, .9, .8, .7, .625] #mm

gamma = 1.305
r_t = .625 #mm
A_t = np.pi * (r_t / 1000)**2 #m^2
k = gamma - 1
P_a = 101354.62277 #Pa
a = 1
for i in r_e:
    AreaRatio.append(i**2 / r_t**2)

for l in range(0,len(Geometries)):
                
    TimeData = []
    ForceData = []
    ChamberPressureData = []
    ChamberTempData = []
    ExitTempData = []
    PredictedForce = []
    
    Geometry = Geometries[l]
    Trial = 1
    
    columns = np.loadtxt('../Refined_Data_Files/Data_Files/{}_trial_{}.txt'
                         .format(Geometry, Trial), delimiter=',')
   
    for column in columns:
        TimeData.append(column[0])
        ForceData.append(column[1])
        ChamberPressureData.append(column[2])
        ChamberTempData.append(column[3] + 273.15)
        ExitTempData.append(column[4] + 273.15)
    
    for i in range(0,len(TimeData)):
        MSquared = (2 / k) * np.abs((ChamberTempData[i] / 
                               ExitTempData[i]) - 1)
        PressureRatio = (1 + (k / 2) * MSquared)**(gamma / k)
        first = (2 * gamma**2) / k
        second = (2 / (gamma + 1))**((gamma + 1) / k)
        third = (1 - (1  / PressureRatio)**(k / gamma))
        SQRTARG = first * second * third
        PredictedForce.append((np.sqrt(SQRTARG) + ((1 / PressureRatio) - 
                            (P_a / ChamberPressureData[i])) * 
                               AreaRatio[l]) * A_t * ChamberPressureData[i])

    plt.plot(TimeData, ForceData, label='Experimental {}'.format(Geometry))
    plt.plot(TimeData, PredictedForce, label = 'Predicted')
    plt.legend(loc='best', fontsize=8)
    plt.figaspect(10.15)    
    plt.savefig('../Plots/Force/Force{}.png'.format(Geometry))
    plt.show()
    plt.close()
