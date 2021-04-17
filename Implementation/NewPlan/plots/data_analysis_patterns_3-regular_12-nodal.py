# -*- coding: utf-8 -*-
"""
Created on Mon Jun 29 15:01:01 2020

@author: joost
"""
import pandas as pd
import numpy as np
from data_load import load_csv
import matplotlib.pyplot as plt

# loading dataframe
filename = 'data_3-regular.csv'
df = load_csv(filename); # eine keer

# df.loc[df['p'] == 10][['gammas']]
label = True
for i in range(9,280,10): 
    xticks = np.arange(1,10+1)
    g = df['gammas'][i]
    b = df['betas'][i]
    
    #plt.title(r"Pattern $\vec{\gamma}, \vec{\beta}$ for 12-nodal 3-regular graphs for p = 10")
    plt.plot(xticks,g, color = 'lightblue', linestyle='dashed')
    plt.plot(xticks,b, color = 'lightcoral', linestyle='dashed')
    if label:
        plt.plot(xticks,g, color = 'blue', linestyle = 'None',marker='o', label = r'$\gamma_i$')
        plt.plot(xticks,b, color = 'tab:red', linestyle = 'None',marker='o', label = r'$\beta_i$')
        label = False
    else:
        plt.plot(xticks,g, color = 'blue', linestyle = 'None',marker='o')
        plt.plot(xticks,b, color = 'tab:red', linestyle = 'None',marker='o')

plt.legend()
plt.grid('on')
plt.ylabel('Angle [radians]')
plt.xlabel('i')

plt.legend()
plt.show()