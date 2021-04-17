# -*- coding: utf-8 -*-
"""
Created on Mon Jun 29 15:01:01 2020

@author: joost
"""
import pandas as pd
import numpy as np
from data_load import load_csv
import matplotlib.pyplot as plt
import matplotlib.pylab as pylab

n = 12
p = 3

# loading dataframe
filename = 'data_trim/data_trim_3-regular_unweighted_INT_'+str(int(n))+'.csv'
df = load_csv(filename); # eine keer

p_max = len(set(df['p']))

# plotting params
fontsize = 18 # 'x-large'
params = {'legend.fontsize': fontsize,
          'figure.figsize': (11, 5),
         'axes.labelsize': fontsize,
         'xtick.labelsize':fontsize-6,
         'ytick.labelsize':fontsize-6}
pylab.rcParams.update(params)

# Figure
fig, (ax1, ax2) = plt.subplots(1, 2)


label = True
for i in range(p-1,len(df),p_max): 
    xticks = np.arange(1,p+1)
    g = df['gammas'][i]
    b = df['betas'][i]
    
    #plt.title(r"Pattern $\vec{\gamma}, \vec{\beta}$ for 12-nodal 3-regular graphs for p = 10")
    ax1.plot(xticks,g, color = 'lightblue', linestyle='dashed')
    ax2.plot(xticks,b, color = 'lightcoral', linestyle='dashed')
    if label:
        ax1.plot(xticks,g, color = 'blue', linestyle = 'None',marker='o', label = r'$\gamma_i$')
        ax2.plot(xticks,b, color = 'tab:red', linestyle = 'None',marker='o', label = r'$\beta_i$')
        label = False
    else:
        ax1.plot(xticks,g, color = 'blue', linestyle = 'None',marker='o')
        ax2.plot(xticks,b, color = 'tab:red', linestyle = 'None',marker='o')

from matplotlib.ticker import MaxNLocator
for ax in [ax1,ax2]:
    ax.grid('on')
    ax.set_xlabel('i')
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    ax.text(0.95, 0.98,'p='+str(p),horizontalalignment='right',verticalalignment='top',transform = ax.transAxes,fontsize = 16, fontstyle='oblique')

ax1.set_ylim([0,np.pi/2])
ax2.set_ylim([0,np.pi/4])
ax1.set_ylabel(r'$\gamma_i$')
ax2.set_ylabel(r'$\beta_i$')
plt.subplots_adjust(wspace = 0.3)

plt.show()