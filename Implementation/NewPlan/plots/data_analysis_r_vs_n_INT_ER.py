# -*- coding: utf-8 -*-
"""
Created on Sat Jul  4 16:22:48 2020

@author: joost
"""

import pandas as pd
import numpy as np
from data_load import load_csv
import matplotlib.pyplot as plt

# # loading dataframes
# # ER 0.75
# n_list = [6,7,8,9,10,11,12,13,14,15]
# frames = [load_csv("data/data_ER-075_unweighted_INT_"+str(n)+".csv") for n in [12,13,14,15]]
# frames.append(load_csv("data/data_ER-075_unweighted_INT_4-12.csv"))
# df = pd.concat(frames)
# p_max = 8

# ER 0.50
n_list = [6,7,8,9,10,11,12,13,14,15]
frames = [load_csv("data/data_ER-050_unweighted_INT_11-14.csv"),
          load_csv("data/data_ER-050_unweighted_INT_15-16.csv"),
          load_csv("data/data_ER-050_unweighted_INT_6-10.csv")]
df = pd.concat(frames)
p_max = 8

# plot configuration
font = {'family' : 'normal',
        'size'   : 16}

plt.rc('font', **font)
plt.figure(figsize=(10,6))
ax = plt.subplot(111)
#colors = ['midnightblue', 'navy', 'darkblue', 'mediumblue', 'blue','dodgerblue', 'royalblue', 'cornflowerblue', 'red']


for c, p in enumerate(range(p_max,0,-1)):
    p_array = [np.mean(df[(df['p'] == p) & (df['n_nodes'] == n)]['Fp']/df[(df['p'] == p) & (df['n_nodes'] == n)]['Cmax']) for n in n_list]
    plt.plot(n_list, p_array, linestyle = 'solid', label = 'p = '+str(p), marker = 'o')
    
#gw_array = [np.mean(df[(df['n_nodes'] == n)]['Fp']/df[(df['n_nodes'] == n)]['Cmax']) for n in n_list]

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


    

