# -*- coding: utf-8 -*-
"""
Created on Sat Jul  4 16:22:48 2020

@author: joost
"""

import pandas as pd
import numpy as np
from data_load import load_csv
import matplotlib.pyplot as plt

# loading dataframes
n_list = [8,10,12,14,16]

df = load_csv('data/data_3-regular_unweighted_RI_8-16.csv')

p_max = 8
p_list = range(p_max,0,-1)

# plot configuration
font = {'size'   : 16}

plt.rc('font', **font)
plt.figure(figsize=(10,6))
ax = plt.subplot(111)


for c, p in enumerate(p_list):
    r_array = np.array([np.mean(df[(df['p'] == p) & (df['n_nodes'] == n)]['Fp']/df[(df['p'] == p) & (df['n_nodes'] == n)]['Cmax']) for n in n_list])
    plt.plot(n_list, r_array, linestyle = 'solid', label = 'p = '+str(p), marker = 'o')
    
#gw_array = np.array([np.mean(df[(df['n_nodes'] == n)]['Fp']/df[(df['n_nodes'] == n)]['Cmax']) for n in n_list]) #wrong

#plt.plot(n_list, gw_array, color = 'orangered', linestyle = 'dotted', linewidth = 2, marker = 's', label = 'GW mean', markersize = 5)
plt.plot(n_list, [0.878]*len(n_list), color = 'coral', linewidth = 2, linestyle = 'dotted', label = 'GW bound')


# legend on side
box = ax.get_position()
ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))

plt.xlabel('Number of nodes $n$')
plt.ylabel('r')
plt.ylim([0.75,1.005])
plt.grid('on')


    

