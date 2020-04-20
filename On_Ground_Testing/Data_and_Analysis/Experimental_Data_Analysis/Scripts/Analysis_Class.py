#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  2 14:01:21 2020

@author: max
"""

import numpy as np
import mpmath as mp
import pandas as pd
import matplotlib.pyplot as plt
plt.style.use('classic')
from CoolProp.CoolProp import PropsSI

class Analyzer:
    
    def __init__(self, Geometry, Trial):
        
        ExitRadii =     [
            5, 5, 4, 4, 3, 3, 2, 2, 1.59323, 1.59323, 
            1, 1, .9, .9, .8, .8, .7, .7, .625, .625
                        ]
        
        self.Geometry = Geometry
        self.Trial = Trial
        self.AreaRatios = []
        self.ForceData = []
        self.TimeData = []
        self.ChamberTempData = []
        self.ActualExitTempData = []
        self.ChamberPressureData = []
        self.Masses = []
        self.Identifiers = []
        self.G = 9.80665
        self.R = 8.31446261815324
        self.W = 0.1178664
        self.gamma = 1.305
        self.P_a = 101354.62277
        self.ThroatRadius = .625e-3
        self.THRESH = .01
        self.UNIT = 1e-1
        self.N = 10
        self.k = self.gamma - 1
        self.m = self.gamma + 1
        self.ThroatArea = np.pi * self.ThroatRadius**2
        self.ExitRadii = list(reversed(ExitRadii))
        self.Identity = self.Geometry + str(self.Trial)
        self.color_value = '#6b8ba4'
        self.thickness = 1.5
        
        for i in self.ExitRadii:
            self.AreaRatios.append((i*10**(-3))**2 / self.ThroatRadius**2)
        
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
            self.ActualExitTempData.append(column[4] + 273.15)
            
        counter = 0
        while counter < self.N:
            for i in range(1, len(self.ChamberPressureData)):
                if 0 <= self.ChamberPressureData[i] <= self.THRESH:
                    pass
                else:
                    change =    (
                                self.ChamberPressureData[i] /   (
                                    self.ChamberPressureData[i-1]
                                                                )
                                )
                    
                    if 1 - self.THRESH <= (
                            change <= 1 + self.THRESH):
                        counter = counter + 1
                        
            self.TotalTime = self.TimeData[i]
            
        self.MassFlowRate = self.Mass / self.TotalTime
        self.ExitTempData = self.SolveExitTemp()
        self.PredictedForce = self.PredictedThrust()
        self.ExperimentalIsp = self.ActualIsp()
        self.PredictedIsp = self.PredictIsp()
        # self.PlotThrust()
        
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
            T_c = self.ChamberTempData[j]
            P_c = self.ChamberPressureData[j]
            Y = self.gamma
            k = self.k
            m = self.m
            w = self.MassFlowRate
            A_e = self.AreaRatio * self.ThroatArea
            rho_c = PropsSI('D','T',T_c,'P',P_c ,'CO2')
            
            test_values = []
            counter = 0
            
            while counter < self.N:
                term_1 = (k / (2*Y*P_c*rho_c))
                term_2 = ((1e2*w) / A_e)**2
                term_3 = mp.root(T_c / T_e, k/m, k=0)
                
                T_e =   (
                        T_c /   (
                                    term_1 * term_2 * term_3 + 1
                                )
                        )

                test_values.append(T_e)
                counter = 0
                
                for i in range(1,len(test_values)):
                    if 0 <= test_values[i] <= self.THRESH:
                        pass
                    elif 1 - self.THRESH <= (
                            test_values[i] / test_values[i-1]
                            ) <= 1 + self.THRESH:
                        counter = counter + 1
            
            ExitTemp.append(T_e)
        
        return ExitTemp
    
    def PredictedThrust(self, T=None):
        
        PredictedForce = []
        for i in range(0,len(self.TimeData)):
            if T is None:
                T_e = self.ExitTempData[i]
            else:
                T_e = self.ActualExitTempData[i]
            T_c = self.ChamberTempData[i]
            P_c = self.ChamberPressureData[i]
            P_a = self.P_a
            A_t = self.ThroatArea
            Y = self.gamma
            k = self.k
            m = self.m
            Q = ((2*Y**2) / k) * (2 / m)**(m/k)
            TR = T_e / T_c
            E = self.AreaRatio
            if T is None:
                NewForce = A_t * P_c *  (
                    mp.root((Q - Q*TR), 2, k=0) +   (
                                                mp.root(TR, k/Y, k=0) - (P_a/P_c)
                                                    ) * E
                                        )
            else:
                NewForce = A_t * P_c *  (
                np.sqrt(Q - Q*TR) +   (
                                            mp.root(TR, k/Y, k=0) - (P_a/P_c)
                                                ) * E
                                    )
            PredictedForce.append(self.UNIT*NewForce)
        return PredictedForce
    
    def FirstThrustFix(self):
        PredictedForce = []
        for i in range(0,len(self.TimeData)):
            T_e = self.ActualExitTempData[i]
            T_c = self.ChamberTempData[i]
            P_c = self.ChamberPressureData[i]
            P_a = self.P_a
            A_t = self.ThroatArea
            Y = self.gamma
            k = self.k
            m = self.m
            Q = ((2*Y**2) / k) * (2 / m)**(m/k)
            TR = T_e / T_c
            E = self.AreaRatio
            
            NewForce = A_t * P_c *  (
                mp.root((np.abs(Q - Q*TR)), 2, k=0) +   (
                                            mp.root(TR, k/Y, k=0) - (P_a/P_c)
                                                ) * E
                                    )
            
            PredictedForce.append(self.UNIT*NewForce)
        return PredictedForce
    
    def PredictIsp(self):
        PredictedIsp = []
        for i in range(0,len(self.TimeData)):
            T_e = self.ExitTempData[i]
            T_c = self.ChamberTempData[i]
            P_c = self.ChamberPressureData[i]
            P_a = self.P_a
            Y = self.gamma
            k = self.k
            W = self.W
            R = self.R
            rho_c = PropsSI('D','T',T_c,'P',P_c ,'CO2')
            self.C_D = np.sqrt((self.gamma * rho_c) / P_c)
            C_D = self.C_D
            
            SQRT_TERM = np.sqrt(((2*Y*R*T_c) / (k*W)) * (1 - (T_e/T_c)))
                        
            NewIsp = (self.AreaRatio / C_D) * (SQRT_TERM + (
                (T_e/T_c)**(Y/k) - (P_a/P_c)))
            
            PredictedIsp.append(NewIsp)
        return PredictedIsp
    
    def ActualIsp(self):
        PointIsp = []
        for i in range(0,len(self.TimeData)):
            PointIsp.append(self.ForceData[i] / self.MassFlowRate)
        
        return PointIsp
    
    def PlotThrust(self):
        
        size = 20
        size_config = .8
        fig = plt.figure(1, figsize=(10,7))
        fig.suptitle('${}\ Thrust\ Curves$'.format(self.Identity), fontsize=size)
        plt.xlim(-1,12)
        if max(self.PredictedForce) > max(self.ForceData):
            ymax = (max(self.PredictedForce))
        else:
            ymax = (max(self.ForceData))
        plt.ylim(-round(.05*ymax, 2), round(1.05 * ymax, 2))
        plt.xlabel('$Time\ (s)$', fontsize=size_config*size)
        plt.ylabel('$Force\ (N)$', fontsize=size_config*size)
        plt.plot(self.TimeData, self.PredictedForce, label='$Theoretical$', lw=self.thickness,
                 linestyle='dotted', color='black')
        plt.plot(self.TimeData, self.ForceData, label='$Emperical$', color=self.color_value)
        plt.legend()
        plt.show()
        
    def Smoother(self, DataSet, N):      
        return pd.Series(DataSet).rolling(window=N).mean().iloc[N-1:].values

    def PlotAnyDataSet(self, DataSet1, Variable1, Unit, path, DataSet2=None, Variable2=None, x_data=None):
        if x_data is None:
            x_data = self.TimeData
        else:
            x_data = np.linspace(-1, 12, len(DataSet1))
            
        size = 20
        size_config = .8
        fig = plt.figure(1, figsize=(11,4))
        plt.xlim(-1,12)
        plt.xlabel('$Time\ (s)$', fontsize=size_config*size)
        
        if Variable1 == 'Temperature':
            plt.ylabel('$Temperature\ ({})$'.format(Unit), fontsize=size_config*size)
        else:
            plt.ylabel('${}\ ({})$'.format(Variable1, Unit), fontsize=size_config*size)

        if DataSet2 is not None:
            fig.suptitle('${}\ {}\ and\ {}\ Data$'.format(self.Identity, Variable1, Variable2), fontsize=size)
            
            plt.plot(x_data, DataSet2, color='black', lw=self.thickness,
                    label='${}\ {}\ Data$'.format(self.Identity, Variable1))
            plt.plot(x_data, DataSet1, color=self.color_value,lw=self.thickness,
                    label='${}\ {}\ Data$'.format(self.Identity, Variable2))
        else:
            fig.suptitle('${}\ {}\ Data$'.format(self.Identity, Variable1), fontsize=size)
    
            plt.plot(x_data, DataSet1, color=self.color_value,lw=self.thickness,
                        label='${}\ {}\ Data$'.format(self.Identity, Variable1))
        plt.legend()
        plt.savefig('{}'.format(path), bbox_inches = "tight")
        plt.close()