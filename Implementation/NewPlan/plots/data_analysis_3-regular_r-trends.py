# -*- coding: utf-8 -*-
"""
Created on Fri Jul  3 08:42:42 2020

@author: joost
"""


import pandas as pd
import numpy as np
from data_load import load_csv
import matplotlib.pyplot as plt

# loading dataframe
pre = "data_trim/data_trim_3-regular_"
post =".csv"
filename = "weighted_INT_8"
df = load_csv(pre+filename+post); # eine keer

p_max = 8

r_sum = np.zeros(p_max)
label = True
for i in range(0,len(df),p_max): 
    Fp = np.array([df['Fp'][i+j] for j in range(p_max)])
    Cmax = np.array([df['Cmax'][i+j] for j in range(p_max)])
    
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
    return a * np.exp(-p / b)


r_mean = r_sum/len(range(0,len(df),p_max))
params, params_covariance = optimize.curve_fit(test_func, xticks, 1-r_mean,
                                               p0=[0.8, 2])
    
plt.plot(xticks,1-r_mean, color = 'maroon', linestyle = 'None', marker = 'o', label = 'mean')
plt.plot(xticks,test_func(xticks,params[0],params[1]), color = 'firebrick', linestyle = 'dashed', label = r'$\alpha e^{-p/p_0}$')

plt.legend()
plt.show()

perr = np.sqrt(np.diag(params_covariance))
print(perr)