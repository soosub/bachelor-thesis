# -*- coding: utf-8 -*-
"""
Created on Fri Jul  3 08:26:06 2020

@author: joost
"""

import pandas as pd
import numpy as np
from data_load import load_csv
import matplotlib.pyplot as plt
from GW import goemans_williamson

plt.close('all')

# loading dataframe
n = 16
pre = "data_trim/data_trim_3-regular_"
post =".csv"
filename = "weighted_INT_"+str(n)
df = load_csv(pre+filename+post); # eine keer

# exponent or exponent of square root
SQR = True

p_max = 8

plt.figure()
plt.hlines(0.878, 0, p_max, colors='lightblue', linestyles='dashed',label = "GW-bound")

# df.loc[df['p'] == 10][['gammas']] - Wybe
for i in range(0,len(df),p_max): 
    Fp = np.array([df['Fp'][i+j] for j in range(p_max)])
    Cmax = np.array([df['Cmax'][i+j] for j in range(p_max)])
    
    r = Fp/Cmax
    xticks = np.arange(1,p_max+1)
    
    #plt.title(r"$F_p$ for 12-nodal 3-regular graphs for $p = 1...10$")
    plt.plot(xticks,r, color = 'lightgreen', linestyle = 'dashed')
    plt.plot(xticks,r, color = 'green', linestyle = 'None', marker = 'o')
    plt.grid('on')
    plt.ylabel(r'$F_p$')
    plt.xlabel('p')
    plt.xlim([0.8,p_max+0.2])

plt.figure()
r_sum = np.zeros(p_max)
label = True
r_GW_mean = 0
for i in range(0,len(df),p_max): 
    Fp = np.array([df['Fp'][i+j] for j in range(p_max)])
    Cmax = np.array([df['Cmax'][i+j] for j in range(p_max)])
    GW = np.mean([goemans_williamson(df['graph'][i]) for _ in range(10)])/Cmax[0]
    print(GW)
    r_GW_mean += GW/len(range(0,len(df),p_max)) 
    r = Fp/Cmax
    r_sum += r
    
    xticks = np.arange(1,p_max+1)
    
    #plt.title(r"$F_p$ for 12-nodal 3-regular graphs for $p = 1...10$")
    plt.yscale("log")
    if label:
        plt.plot(xticks,1-r, color = 'peachpuff', linestyle = 'dashed')
        plt.plot(xticks,1-r, color = 'darkorange', linestyle = 'None', marker = 'o', label = 'random instance')
        label = False
    else:
        plt.plot(xticks,1-r, color = 'peachpuff', linestyle = 'dashed')
        plt.plot(xticks,1-r, color = 'darkorange', linestyle = 'None', marker = 'o')
    plt.grid(True,which="both", ls="-")
    plt.ylabel(r'$1-r$')
    plt.xlabel('p')
   
# Mean, including a fit
from scipy import optimize
def test_func(p, a, b):
    if not SQR:
        return a * np.exp(-p / b)
    if SQR:
        return a * np.exp(-np.sqrt(p / b))

if not SQR:
    label = r'$\alpha e^{-p/p_0}$'
if SQR:
    label = r'$\alpha e^{-\sqrt{p/p_0}}$'

r_mean = r_sum/len(range(0,len(df),p_max))
params, params_covariance = optimize.curve_fit(test_func, xticks, 1-r_mean,
                                               p0=[0.8, 2])
    
plt.plot(xticks,1-r_mean, color = 'maroon', linestyle = 'None', marker = 'o', label = 'mean')
plt.plot(xticks,test_func(xticks,params[0],params[1]), color = 'firebrick', linestyle = 'dashed', label = label)

plt.hlines(1-0.878, 1, p_max, colors='lightblue', linestyles='dashed',label = "GW bound",zorder=3)
plt.hlines(1-r_GW_mean,1, p_max,colors = 'dodgerblue', linestyles='dashed', label = r'$r_{GW}$ mean',zorder=3)

plt.legend()
plt.show()

perr = np.sqrt(np.diag(params_covariance))
print('parameters', params)
print('std', perr)