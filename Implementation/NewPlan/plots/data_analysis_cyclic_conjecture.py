# -*- coding: utf-8 -*-
"""
Created on Tue Jun 30 23:19:35 2020

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

def Mp(n,p):
    return n*(2*p+1)/(2*p+2)

colors = ["tab:blue","tab:orange","tab:green","tab:red","tab:purple","tab:brown","tab:pink","tab:cyan"]

# even
c = 0
fig = plt.figure()
ax = plt.subplot(111)
for i in range(p_max,len(df),2*p_max): 
    n = df.n_nodes[i]
    p = df.p[i]
    
    print(n)
    Fp = [df['Fp'][i+j]for j in range(p_max)]
    xticks = np.arange(1,p_max+1)
    
    #plt.title(r"$F_p$ for 12-nodal 3-regular graphs for $p = 1...10$")
    plt.plot(xticks,Fp, color = colors[c], linestyle = "None", marker = 'o', label = 'n = '+str(int(n)))
    plt.plot(xticks,Mp(n,xticks), color = colors[c], linestyle = 'dashed', label = r"$M_{p}(n="+str(int(n))+")$")
    c += 1

# Shrink current axis by 20%
box = ax.get_position()
ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])

# Put a legend to the right of the current axis
ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
plt.grid('on')
plt.ylabel(r'$F_p$')
plt.xlabel('p')
    
