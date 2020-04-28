#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 26 17:29:19 2020

@author: max
"""


from scipy import stats
import numpy as np
import matplotlib.pyplot as plt
plt.style.use('classic')

r = 0.10 #m
m_pd = .720 #kg
g = 9.81 #m/s^2

Time = []
w_z = []
alpha_w = []
I_w = []

Gases = ['H2', 'He', 'N2', 'CO2']
Gas_Isps = [296, 179, 80, 67]

path = 'Titan1_Flight_Data_Report_z_w.csv'
columns = np.loadtxt(path, delimiter=',', dtype='str', skiprows=1)

for column in columns:
    Time.append(float(column[0]))
    w_z.append(float(column[1]))
    
Time = np.array(Time) / 3600 
w_z = np.array(w_z) 

for i in range(0,len(w_z)-1):
    del_w = np.abs((w_z[i+1] - w_z[i]) / (Time[i+1] - Time[i]))
    alpha_w.append(del_w)

a_w = np.array(alpha_w) * r

F_w = a_w * m_pd

# for i in range(0,186):
#     impulse = (F_w[i] + F_w[i+1]) * (Time[i+1] - Time[i])
#     I_w.append(impulse)
    
# I_w = np.array(I_w)
# I_total = np.sum(I_w)

# for i in range(0, len(Gas_Isps)):
#     mass_gas = ((I_total / Gas_Isps[i]) / g) * 10**(3)
#     print('Mass of {} = {} g'.format(Gases[i],round(mass_gas,2)))
#============================================================================#  
for i in range(167,186):
    impulse = (F_w[i] + F_w[i+1]) * (Time[i+1] - Time[i])
    I_w.append(impulse)
    
I_w = np.array(I_w)
I_total = np.sum(I_w)

for i in range(0, len(Gas_Isps)):
    mass_gas = ((I_total / Gas_Isps[i]) / g) * 10**(3)
    print('Mass of {} = {} g'.format(Gases[i],round(mass_gas,2)))