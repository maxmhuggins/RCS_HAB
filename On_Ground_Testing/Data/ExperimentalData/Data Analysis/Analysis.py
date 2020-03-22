import numpy as np
import matplotlib.pyplot as plt

TimeData = []
ForceData = []
PressureData = []
CO2TempData = []
PipeTempData = []

columns = np.loadtxt('../test_trial_2.txt', delimiter=',')

for column in columns:
    TimeData.append(column[0])
    ForceData.append(column[1])
    PressureData.append(column[2])
    CO2TempData.append(column[3])
    PipeTempData.append(column[4])


plt.scatter(TimeData, ForceData, label='Force', s=1)
plt.savefig('../test_trial_2Force.png')
plt.close()
plt.plot(TimeData, PressureData, label='Pressure')
plt.savefig('../test_trial_2Pressure.png')
plt.close()
plt.plot(TimeData, CO2TempData, label='CO2Temp')
plt.savefig('../test_trial_2CO2Temp.png')
plt.close()
plt.plot(TimeData, PipeTempData, label='PipeTemp')
plt.savefig('../test_trial_2PipeTemp.png')
plt.close()

