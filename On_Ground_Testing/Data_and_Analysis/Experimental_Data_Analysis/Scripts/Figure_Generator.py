#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 18 15:58:48 2020

@author: max
"""
import matplotlib.pyplot as plt
import Analysis_Class as AC
#=============================================================================#
N = 100
size = 20
size_config = .8
legendfont = 10
thickness = 1.5
ymax = 20
color_value = '#6b8ba4'
#=============================================================================#
O1 = AC.Analyzer('O',1)
O2 = AC.Analyzer('O',2)
O11 = AC.Analyzer('O1',1)
O12 = AC.Analyzer('O1',2)
O21 = AC.Analyzer('O2',1)
O22 = AC.Analyzer('O2',2)
O31 = AC.Analyzer('O3',1)
O32 = AC.Analyzer('O3',2)
O41 = AC.Analyzer('O4',1)
O42 = AC.Analyzer('O4',2)
U11 = AC.Analyzer('U1',1)
U12 = AC.Analyzer('U1',2)
U21 = AC.Analyzer('U2',1)
U22 = AC.Analyzer('U2',2)
U31 = AC.Analyzer('U3',1)
U32 = AC.Analyzer('U3',2)
U41 = AC.Analyzer('U4',1)
U42 = AC.Analyzer('U4',2)
N1 = AC.Analyzer('N',1)
N2 = AC.Analyzer('N',2)
#=================================================#
IdentifiersList =   [
    N1, N2, U41, U42, U31, U32, U21, U22, U11, U12, 
    O1, O2, O11, O12, O21, O22, O31, O32, O41, O42
                    ]
#=================================================#   
#=================================================#
IdentifiersListStrings =   [
    'N1', 'N2', 'U41', 'U42', 'U31', 'U32', 'U21', 'U22', 'U11', 'U12', 
    'O1', 'O2', 'O11', 'O12', 'O21', 'O22', 'O31', 'O32', 'O41', 'O42'
                    ]
#=================================================#   
#=============================================================================#
path = '../../../Write_Ups/CGT_Document/Figures/ExampleTemp.eps'

U41.PlotAnyDataSet(U41.ChamberTempData, 'T_c', 'K', path)

SmoothChamberTemp = U41.Smoother(U41.ChamberTempData, N)
#=============================================================================#
path = '../../../Write_Ups/CGT_Document/Figures/SmoothTemp.eps'

U41.PlotAnyDataSet(SmoothChamberTemp, 'T_c\ Smoothed', 'K', path, x_data=1)
#=============================================================================#
path = '../../../Write_Ups/CGT_Document/Figures/TwoSmoothedTemps.eps'
SmoothExitTemp = U41.Smoother(U41.ActualExitTempData, N)
U41.PlotAnyDataSet(SmoothChamberTemp, 'T_c\ Smoothed', 'K', path, 
                    SmoothExitTemp, 'T_e\ Smoothed', x_data=1)
#=============================================================================#
path = '../../../Write_Ups/CGT_Document/Figures/FirstAttempt.eps'
U41.PlotAnyDataSet(U41.PredictedThrust(T=1), 'Theoretical\ Thrust', 'N', 
                    path, U41.ForceData, 'Actual\ Thrust')
#=============================================================================#
path = '../../../Write_Ups/CGT_Document/Figures/FirstFix.eps'
FixedForce = U41.FirstThrustFix()
U41.PlotAnyDataSet(FixedForce, 'Theoretical\ Thrust', 'N', path, 
                    U41.ForceData, 'Actual\ Thrust')
#=============================================================================#
path = '../../../Write_Ups/CGT_Document/Figures/FirstThreeCurves.eps'
#=================================================#
fig = plt.figure(1, figsize=(11,4))
fig.suptitle('$Thrust\ Curves$', fontsize=size)
plt.subplot(131)
plt.ylim(-round(.05*ymax, 2), round(1.05 * ymax, 2))
plt.xlim(-1,12)
plt.ylabel('$Force\ (N)$', fontsize=size_config*size)
plt.plot(O1.TimeData, O1.FirstThrustFix(), label='$Theoretical$', 
          lw=thickness, linestyle='dotted', color='black')
plt.plot(O1.TimeData, O1.ForceData, label='$Optimum\ Expansion$', 
          color=color_value, lw=thickness)
plt.legend(loc='best', fontsize=legendfont)
#=================================================#
plt.subplot(132)
plt.ylim(-round(.05*ymax, 2), round(1.05 * ymax, 2))
plt.xlim(-1,12)
plt.xlabel('$Time\ (s)$', fontsize=size_config*size)
plt.plot(O41.TimeData, O41.FirstThrustFix(), label='$Theoretical$', 
          lw=thickness, linestyle='dotted', color='black')
plt.plot(O41.TimeData, O41.ForceData, label='$Over\ Expanded$', 
          lw=thickness, color=color_value)
plt.legend(loc='best', fontsize=legendfont)
#=================================================#
plt.subplot(133)
plt.ylim(-round(.05*ymax, 2), round(1.05 * ymax, 2))
plt.xlim(-1,12)
plt.plot(U41.TimeData, U41.FirstThrustFix(), label='$Theoretical$', 
          lw=thickness, linestyle='dotted', color='black')
plt.plot(U41.TimeData, U41.ForceData, label='$Under\ Expanded$', 
          lw=thickness, color=color_value)
plt.legend(loc='best', fontsize=legendfont)
#=================================================#
plt.savefig('{}'.format(path), bbox_inches = "tight")
plt.close()
#=============================================================================#
path = '../../../Write_Ups/CGT_Document/Figures/SecondThreeCurves.eps'
#=================================================#
fig = plt.figure(2, figsize=(11,4))
fig.suptitle('$Thrust\ Curves$', fontsize=size)
plt.subplot(131)
plt.ylim(-round(.05*ymax, 2), round(1.05 * ymax, 2))
plt.xlim(-1,12)
plt.ylabel('$Force\ (N)$', fontsize=size_config*size)
plt.plot(O1.TimeData, O1.PredictedForce, label='$Theoretical$', 
          lw=thickness, linestyle='dotted', color='black')
plt.plot(O1.TimeData, O1.ForceData, label='$Optimum\ Expansion$', 
          color=color_value, lw=thickness)
plt.legend(loc='best', fontsize=legendfont)
#=================================================#
plt.subplot(132)
plt.ylim(-round(.05*ymax, 2), round(1.05 * ymax, 2))
plt.xlim(-1,12)
plt.xlabel('$Time\ (s)$', fontsize=size_config*size)
plt.plot(O41.TimeData, O41.PredictedForce, label='$Theoretical$', 
          lw=thickness, linestyle='dotted', color='black')
plt.plot(O41.TimeData, O41.ForceData, label='$Over\ Expanded$', 
          lw=thickness, color=color_value)
plt.legend(loc='best', fontsize=legendfont)
#=================================================#
plt.subplot(133)
plt.ylim(-round(.05*ymax, 2), round(1.05 * ymax, 2))
plt.xlim(-1,12)
plt.plot(U41.TimeData, U41.PredictedForce, label='$Theoretical$', 
          lw=thickness, linestyle='dotted', color='black')
plt.plot(U41.TimeData, U41.ForceData, label='$Under\ Expanded$', 
          lw=thickness, color=color_value)
plt.legend(loc='best', fontsize=legendfont)
#=================================================#
plt.savefig('{}'.format(path), bbox_inches = "tight")
plt.close()
#=============================================================================#
path = '../../../Write_Ups/CGT_Document/Figures/Isp.txt'
IspList = []
file = open(path, 'w')
file.write('Geometry' + ',' + 'Specific Impulse' + '\n')

for i in range(0,len(IdentifiersList)):
    append = IdentifiersList[i].ExperimentalIsp
    IspList.append(append)
    print(append)
    
    file.write(IdentifiersListStrings[i] + ',' + str(round(append, 1)) + '\n')

file.close()
    
    
    
    
    
    
    
    
    
    
    
    
    
    