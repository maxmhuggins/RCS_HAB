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
        self.ForceData = []
        self.TimeData = []
        self.Masses = []
        self.Identifiers = []
        self.Identity = self.Geometry + str(self.Trial)
        self.G = 9.80665

        columns = np.loadtxt(
            '../Refined_Data_Files/Calibration_Files/Mass.txt'
            , delimiter=',', dtype='str')
        
        for column in columns:
            self.Identifiers.append(column[0])
            self.Masses.append(column[1])
            
        for i in range(0,len(self.Identifiers)):
            if self.Identifiers[i] == self.Identity:
                self.Mass = float(self.Masses[i])
            
        columns = np.loadtxt('../Refined_Data_Files/Data_Files/{}_trial_{}.txt'
                         .format(self.Geometry, self.Trial), delimiter=',')
        for column in columns:
            self.TimeData.append(column[0])
            self.ForceData.append(column[1])
        
        self.Isp = self.SpecificImpulse()
        
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
    

O1 = Analyzer('O',1)
O2 = Analyzer('O',2)
O11 = Analyzer('O1',1)
O12 = Analyzer('O1',2)
O21 = Analyzer('O2',1)
O22 = Analyzer('O2',2)
O31 = Analyzer('O3',1)
O32 = Analyzer('O3',2)
O41 = Analyzer('O4',1)
O42 = Analyzer('O4',2)
U11 = Analyzer('U1',1)
U12 = Analyzer('U1',2)
U21 = Analyzer('U2',1)
U22 = Analyzer('U2',2)
U31 = Analyzer('U3',1)
U32 = Analyzer('U3',2)
U41 = Analyzer('U4',1)
U42 = Analyzer('U4',2)
N1 = Analyzer('N',1)
N2 = Analyzer('N',2)


SpecificImpulses = [
    N1.Isp, N2.Isp, U41.Isp, U42.Isp, U31.Isp, U32.Isp, 
    U21.Isp, U22.Isp, U11.Isp, U12.Isp, O1.Isp, O2.Isp, 
    O11.Isp, O12.Isp, O21.Isp, O22.Isp, O31.Isp, O32.Isp, 
    O41.Isp, O42.Isp
    ]
x = range(0,20)

plt.scatter(x, SpecificImpulses)