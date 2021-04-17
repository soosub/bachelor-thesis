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
n_list = [4,5,6,7,8,9,10,11,12]

df1 = load_csv("data/data_complete_unweighted_INT_4-12.csv")
df2 = pd.DataFrame() 

frames = [df1, df2]
df = pd.concat(frames)
p_max = 8
p_list = range(p_max,0,-1)

# plot configuration
font = {'family' : 'normal',
        'size'   : 16}

plt.rc('font', **font)
plt.figure(figsize=(10,6))
ax = plt.subplot(111)


for c, p in enumerate(p_list):
    r_array = np.array([np.mean(df[(df['p'] == p) & (df['n_nodes'] == n)]['Fp']/df[(df['p'] == p) & (df['n_nodes'] == n)]['Cmax']) for n in n_list])
    plt.plot(n_list, 1-r_array, linestyle = 'solid', label = 'p = '+str(p), marker = 'o')
    
gw_array = np.array([np.mean(df[(df['n_nodes'] == n)]['Fp']/df[(df['n_nodes'] == n)]['Cmax']) for n in n_list])

plt.yscale('log')
plt.plot(n_list, 1-gw_array, color = 'orangered', linestyle = 'dotted', linewidth = 2, marker = 's', label = 'GW', markersize = 5)
plt.plot(n_list, [1-0.878]*len(n_list), color = 'coral', linewidth = 2, linestyle = 'dotted', label = 'GW bound')


# legend on side
box = ax.get_position()
ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))

plt.xlabel('Number of nodes $n$')
plt.ylabel('1-r')
plt.grid('on')


    

