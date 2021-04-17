# -*- coding: utf-8 -*-
"""
Created on Tue Jun 30 19:54:28 2020

@author: joost
"""

from data_load import load_csv
import numpy as np
import matplotlib.pyplot as plt

filename = 'data_2-regular.csv'
df = load_csv(filename)

n_graphs = 18
p_max = 10

def cmax(n):
    return n - n%2

# odd
for i in range(0,len(df),2*p_max): 
    n = df.n_nodes[i]
    print(n, cmax(n))
    r = [df['Fp'][i+j]/cmax(n) for j in range(p_max)]
    print(r)
    xticks = np.arange(1,p_max+1)
    
    #plt.title(r"$F_p$ for 12-nodal 3-regular graphs for $p = 1...10$")
    plt.plot(xticks,r, linestyle = 'dashed', marker = 'o', label = 'n = '+str(int(n)))
    plt.grid('on')
    plt.ylabel(r'$r$')
    plt.ylim([0.72,1.02])
    plt.xlabel('p')
    plt.legend()

plt.figure()
# even
for i in range(p_max,len(df),2*p_max): 
    n = df.n_nodes[i]
    print(n, cmax(n))
    r = [df['Fp'][i+j]/cmax(n) for j in range(p_max)]
    print(r)
    xticks = np.arange(1,p_max+1)
    
    #plt.title(r"$F_p$ for 12-nodal 3-regular graphs for $p = 1...10$")
    plt.plot(xticks,r, linestyle = 'dashed', marker = 'o', label = 'n = '+str(int(n)))
    plt.grid('on')
    plt.ylim([0.72,1.02])
    plt.ylabel(r'$r$')
    plt.xlabel('p')
    plt.legend()