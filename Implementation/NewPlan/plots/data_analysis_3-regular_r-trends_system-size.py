# -*- coding: utf-8 -*-
"""
Created on Fri Jul  3 09:11:08 2020

@author: joost
"""

import numpy as np
from data_load import load_csv
import matplotlib.pyplot as plt
from GW import goemans_williamson

# exponent or exponent of square root
SQR = True
plt.figure()
p_max = 8
graph_weight = 'weighted'
colors = ["tab:blue","tab:orange","tab:green","tab:red","tab:purple","tab:pink","tab:cyan"]


for c,n in enumerate([8,10,12,14,16]):
    # loading dataframe
    pre = "data_trim/data_trim_3-regular_"
    post =".csv"
    filename = graph_weight+"_INT_"+str(n)
    df = load_csv(pre+filename+post);
    
    r_sum = np.zeros(p_max)
    r_GW = 0
    label = True
    
    # looping over the different graphs
    for k,i in enumerate(range(0,len(df),p_max)): 
        print(k,i)
        Fp = np.array([df['Fp'][i+j] for j in range(p_max)])
        Cmax = np.array([df['Cmax'][i+j] for j in range(p_max)])
        
        G = df['graph'][i]
        
        r = Fp/Cmax
        r_GW += np.mean([goemans_williamson(G) for i in range(10)])/Cmax[0]
        r_sum += r
        
        xticks = np.arange(1,p_max+1)
    r_mean = r_sum/len(range(0,len(df),p_max))
    r_GW = r_GW/len(range(0,len(df),p_max))
        
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
    
    
    params, params_covariance = optimize.curve_fit(test_func, xticks, 1-r_mean,
                                                   p0=[0.8, 2])
    plt.yscale("log")
    plt.plot(xticks,1-r_mean, linestyle = 'None', color = colors[c], marker = 'o', label = 'n = '+str(n))
    plt.hlines(1-r_GW, 1,p_max, linestyle = 'dashed', color = colors[c])#, label = r'$1-r_{GW}$ n = '+str(n))
    plt.plot(xticks,test_func(xticks,params[0],params[1]), color = colors[c], linestyle = 'solid')
    plt.grid(True,which="both", ls="-")
    
plt.hlines(1-0.878, 1,p_max,colors='coral', linestyles = 'dotted', label = 'GW bound')
plt.ylabel(r'$1-r$')
plt.xlabel('p')
plt.legend()
plt.show()