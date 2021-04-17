# -*- coding: utf-8 -*-
"""
Created on Mon Jun 29 15:50:15 2020

@author: joost
"""

import pandas as pd
import numpy as np
from data_load import load_csv
import matplotlib.pyplot as plt
from math import ceil # this is easiest (and luckily turns out right in this case, in the future I'll add another column with C_max)
import matplotlib.pylab as pylab
from GW import goemans_williamson

# loading dataframe
filename = 'data/data_3-regular_unweighted_INT_12.csv'
df = load_csv(filename); # eine keer

p_max = 10
# plotting params
fontsize = 20 # 'x-large'
params = {'legend.fontsize': fontsize,
          'figure.figsize': (10, 8),
         'axes.labelsize': fontsize+4,
         'axes.titlesize':fontsize+4,
         'xtick.labelsize':fontsize-2,
         'ytick.labelsize':fontsize-2}
#pylab.rcParams.update(params)

# figure 1
plt.figure() 
for i in range(0,280,10): 
    Fp = [df['Fp'][i+j]/ceil(df['Fp'][i+9]) for j in range(10)]
    xticks = np.arange(1,10+1)
    
    #plt.title(r"$F_p$ for 12-nodal 3-regular graphs for $p = 1...10$")
    plt.plot(xticks,Fp, color = 'lightgreen', linestyle = 'dashed')
    plt.plot(xticks,Fp, color = 'green', linestyle = 'None', marker = 'o')
    plt.grid('on')
    plt.ylabel(r'$r$')
    plt.xlabel('p')


# figure 2
plt.figure()  
 

r_sum = np.zeros(10)
label = True
r_GW_mean = 0
for i in range(0,280,10): 
    Fp = [df['Fp'][i+j] for j in range(10)]
    Cmax = [ceil(df['Fp'][i+9]) for j in range(10)]
    GW = goemans_williamson(df['graph'][i])
    
    r_GW_mean += GW/Cmax[0]/len(range(0,len(df),p_max))    
    r = np.array([Fp[i]/Cmax[i] for i in range(10)])
    r_sum += r
    
    xticks = np.arange(1,10+1)
    
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
    return a * np.exp(-p / b)


r_mean = r_sum/len(range(0,280,10))
params, params_covariance = optimize.curve_fit(test_func, xticks, 1-r_mean,
                                               p0=[0.8, 2])
    
plt.plot(xticks,1-r_mean, color = 'maroon', linestyle = 'None', marker = 'o', label = 'mean')
plt.plot(xticks,test_func(xticks,params[0],params[1]), color = 'firebrick', linestyle = 'dashed', label = r'$\alpha e^{-p/p_0}$')

plt.hlines(1-0.878, 1, p_max, colors='lightblue', linestyles='dashed',label = "GW bound",zorder=3)
plt.hlines(1-r_GW_mean,1, p_max,colors = 'dodgerblue', linestyles='dashed', label = r'$r_{GW}$ mean',zorder=3)

plt.legend()
plt.show()

perr = np.sqrt(np.diag(params_covariance))
print('parameters', params)
print('std', perr)
