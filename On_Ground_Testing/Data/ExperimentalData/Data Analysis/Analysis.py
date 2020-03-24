import numpy as np
import matplotlib.pyplot as plt

TimeData = []
ForceData = []
PressureData = []
CO2TempData = []
PipeTempData = []

columns = np.loadtxt('../O3_trial_1.txt', delimiter=',')

for column in columns:
    TimeData.append(column[0])
    ForceData.append(column[1])
    PressureData.append(column[2])
    CO2TempData.append(column[3])
    PipeTempData.append(column[4])


plt.scatter(TimeData, ForceData, label='Force', s=1)
plt.savefig('../O3_trial_1Force.png')
plt.close()
plt.plot(TimeData, PressureData, label='Pressure')
plt.savefig('../O3_trial_1Pressure.png')
plt.close()
plt.plot(TimeData, CO2TempData, label='CO2Temp')
plt.savefig('../O3_trial_1CO2Temp.png')
plt.close()
plt.plot(TimeData, PipeTempData, label='PipeTemp')
plt.savefig('../O3_trial_1PipeTemp.png')
plt.close()

