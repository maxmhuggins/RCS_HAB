#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 28 14:20:26 2020

@author: max
"""

import numpy as np
import matplotlib.pyplot as plt
# from scipy.optimize import curve_fit
import pandas as pd

Geometries = ['O4', 'O3', 'O2', 'O1', 'O', 'U1', 'U2', 'U3', 'U4', 'N']

def running_mean(x, N):
    return pd.Series(x).rolling(window=N).mean().iloc[N-1:].values

for j in [1,2]:
    
    for l in range(0,len(Geometries)):
                    
        TimeData = []
        ForceData = []
        ChamberPressureData = []
        ChamberTempData = []
        ExitTempData = []
        PredictedForce = []
        
        Geometry = Geometries[l]
        Trial = j
        
        columns = np.loadtxt('../Refined_Data_Files/Data_Files/{}_trial_{}.txt'
                             .format(Geometry, Trial), delimiter=',')

        for column in columns:
            TimeData.append(column[0])
            ForceData.append(column[1])
            ChamberPressureData.append(column[2])
            ChamberTempData.append(column[3] + 273.15)
            ExitTempData.append(column[4] + 273.15)
        
        SmoothedChamberTemp = running_mean(np.array(ChamberTempData), 100)
        SmoothedExitTemp = running_mean(np.array(ExitTempData), 100)
        
        SmoothedTimeData1 = np.linspace(TimeData[0], TimeData[len(TimeData)-1], 
                                       len(SmoothedChamberTemp))
        SmoothedTimeData2 = np.linspace(TimeData[0], TimeData[len(TimeData)-1], 
                                       len(SmoothedExitTemp))
        
        # plt.plot(TimeData, ExitTempData, label='Raw')
        # plt.plot(TimeData, ChamberTempData, label='Raw')
        plt.plot(SmoothedTimeData1, SmoothedChamberTemp, label='Smoothed')
        plt.plot(SmoothedTimeData2, SmoothedExitTemp, label='Smoothed')
        # plt.ylim(0,4)
        # plt.xlim(-1,12)
        plt.legend(loc='best', fontsize=8)
        plt.figaspect(10.15)
        plt.savefig('../Plots/Temperature/Temps{}.eps'.format(Geometry))
        plt.show()
        plt.close()






