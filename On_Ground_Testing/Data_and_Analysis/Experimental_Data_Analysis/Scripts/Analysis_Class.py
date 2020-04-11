#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  2 14:01:21 2020

@author: max
"""

import numpy as np
import matplotlib.pyplot as plt


class Analyzer:
    def __init__(self, Geometry, Trial):
        self.Geometry = Geometry
        self.Trial = Trial
        self.AreaRatios = []
        self.ForceData = []
        self.TimeData = []
        self.ChamberTempData = []
        self.ChamberPressureData = []
        self.Masses = []
        self.Identifiers = []
        self.Identity = self.Geometry + str(self.Trial)
        ExitRadii = [
            5, 5, 4, 4, 3, 3, 2, 2, 1.59323, 1.59323, 1, 1, .9, .9, .8, 
            .8, .7, .7, .625, .625
            ]
        self.ExitRadii = list(reversed(ExitRadii))
        self.G = 9.80665
        self.gamma = 1.305
        self.P_a = 101354.62277
        self.CO2Density = 20.20
        self.ThroatRadius = .625e-3
        self.ThroatArea = np.pi * (self.ThroatRadius*10**(-3))**2
        self.k = self.gamma - 1
        self.m = self.gamma + 1
        self.THRESH = .5
        self.N = 5
        
        for i in self.ExitRadii:
            self.AreaRatios.append(i**2 / self.ThroatRadius**2)
        
        columns = np.loadtxt(
            '../Refined_Data_Files/Calibration_Files/Mass.txt'
            , delimiter=',', dtype='str')
        
        for column in columns:
            self.Identifiers.append(column[0])
            self.Masses.append(column[1])
            
        for i in range(0,len(self.Identifiers)):
            if self.Identifiers[i] == self.Identity:
                self.Mass = float(self.Masses[i])
                self.ExitArea = np.pi * (self.ExitRadii[i]*10**(-3))**2
                self.AreaRatio = self.AreaRatios[i]
                    
        columns = np.loadtxt('../Refined_Data_Files/Data_Files/{}_trial_{}.txt'
                         .format(self.Geometry, self.Trial), delimiter=',')
        
        for column in columns:
            self.TimeData.append(column[0])
            self.ForceData.append(column[1])
            self.ChamberPressureData.append(column[2])
            self.ChamberTempData.append(column[3] + 273.15)
            
        
        counter = 0
        while counter < self.N:
            for i in range(1, len(self.ChamberPressureData)):
                change = (
                    self.ChamberPressureData[i] / self.ChamberPressureData[i-1]
                    )
                if 1 - self.THRESH <= (
                        change <= 1 + self.THRESH
                        ):
                    counter = counter + 1
                    
            self.TotalTime = self.TimeData[i]
            
        self.MassFlowRate = self.Mass / self.TotalTime
        self.Isp = self.SpecificImpulse()
        self.MFConstant = self.MassFlowRate / (
            np.sqrt(2 * self.gamma * self.CO2Density * self.P_a)
            )
        self.ExitTempData = self.SolveExitTemp()
        self.PredictedForce = self.PredictedThrust()
        
    def TrapezoidalSum(self):
        summer = 0
        for i in range(0,len(self.TimeData)-1):
            AreaSection = .5 * (self.ForceData[i] + self.ForceData[i+1]) * (
                self.TimeData[i+1] - self.TimeData[i])
            summer = summer + AreaSection
        return summer
    
    def SpecificImpulse(self):
        Isp = self.TrapezoidalSum() / (self.Mass * self.G)
        return Isp
    
    def SolveExitTemp(self):
        ExitTemp = []
        for j in range(0,len(self.ChamberTempData)):
            T_e = 1
            test_values = []
            counter = 0
            while counter < self.N:
                
                T_e = self.ChamberTempData[j] * (
                    (2 / self.k) * ((self.ExitArea) / self.MFConstant
                        )**2 * ((self.ChamberTempData[j]/T_e) - 1))**(
                            (1-self.gamma) / self.m)
                test_values.append(T_e)
                counter = 0
                for i in range(1,len(test_values)):
                    if 1 - self.THRESH <= (
                            test_values[i] / test_values[i-1]
                            ) <= 1 + self.THRESH:
                            
                        counter = counter + 1
                        # print(counter)
            ExitTemp.append(T_e)
        return ExitTemp
    
    def PredictedThrust(self):
        PredictedForce = []
        for i in range(0,len(self.TimeData)):
            BIG = np.sqrt(
                ((2*self.gamma**2)/(self.k))*(2/self.m)**(self.m/self.k)*(1-(
                self.ExitTempData[i]/self.ChamberTempData[i]))
                )+ ((
                    self.ExitTempData[i]/self.ChamberTempData[i]
                    )**(self.gamma/self.k)-(
                        self.P_a/self.ChamberPressureData[i]
                        ))*self.AreaRatio
            NewForce = self.ThroatArea * self.ChamberPressureData[i] * BIG
            PredictedForce.append(NewForce)
        return PredictedForce

O1 = Analyzer('O',1)
# O2 = Analyzer('O',2)
# O11 = Analyzer('O1',1)
# O12 = Analyzer('O1',2)
# O21 = Analyzer('O2',1)
# O22 = Analyzer('O2',2)
# O31 = Analyzer('O3',1)
# O32 = Analyzer('O3',2)
# O41 = Analyzer('O4',1)
# O42 = Analyzer('O4',2)
# U11 = Analyzer('U1',1)
# U12 = Analyzer('U1',2)
# U21 = Analyzer('U2',1)
# U22 = Analyzer('U2',2)
# U31 = Analyzer('U3',1)
# U32 = Analyzer('U3',2)
# U41 = Analyzer('U4',1)
# U42 = Analyzer('U4',2)
N1 = Analyzer('N',1)
# N2 = Analyzer('N',2)


# SpecificImpulses = [
#     N1.Isp, N2.Isp, U41.Isp, U42.Isp, U31.Isp, U32.Isp, 
#     U21.Isp, U22.Isp, U11.Isp, U12.Isp, O1.Isp, O2.Isp, 
#     O11.Isp, O12.Isp, O21.Isp, O22.Isp, O31.Isp, O32.Isp, 
#     O41.Isp, O42.Isp
#     ]
# x = range(0,20)

# plt.plot(N1.TimeData, N1.ExitTempData, label='exit')
# plt.plot(N1.TimeData, N1.ChamberTempData, label='chamber')
# plt.legend()
# plt.show()
# plt.close()

plt.plot(O1.TimeData, O1.PredictedForce, label='predicted')
plt.plot(O1.TimeData, O1.ForceData, label='data') WRONG
plt.legend()
plt.show()
plt.close()
# plt.scatter(x, SpecificImpulses)