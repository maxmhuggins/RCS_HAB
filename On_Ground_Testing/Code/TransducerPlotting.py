import numpy as np
import matplotlib.pyplot as plt

TimeData = []
PressureData = []

lines = np.loadtxt('../Data/PressureTesting.txt', delimiter=',')
for line in lines:
    TimeData.append(line[0])
    PressureData.append(line[1])

plt.scatter(TimeData, PressureData)

plt.savefig('../Data/TransducerPlot1.eps')
