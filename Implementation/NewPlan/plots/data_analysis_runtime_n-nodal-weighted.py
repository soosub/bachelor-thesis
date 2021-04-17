# -*- coding: utf-8 -*-
"""
Created on Fri Jul  3 16:34:30 2020

@author: joost
"""

import pandas as pd
import numpy as np
from data_load import load_csv
import matplotlib.pyplot as plt

# plot configuration
font = {'family' : 'normal',
        'size'   : 16}

plt.rc('font', **font)
plt.figure(figsize=(10,6))

# loading dataframe
n = 15
filename = "data/data_3-regular_weighted_INT"
df = load_csv(filename); # eine keer


p_max = 8 #int(np.max(df['p']))
seed_max = 10
N = len(set(df['seed']))

mean_runtime = np.zeros(p_max)
mean_cum_time = np.zeros(p_max)


df_new = df[(df['n_nodes'] == n) & (df['seed'] < seed_max) & (df['p'] <= p_max)]['time'].iloc()

# df.loc[df['p'] == 10][['gammas']] - Wybe
for i in range(0,seed_max*p_max,p_max):
    runtime = np.array([df_new[i+j] for j in range(p_max)])
    cum_time= np.array([np.sum(runtime[:k+1]) for k in range(p_max)])
    
    mean_runtime += runtime/N
    mean_cum_time += cum_time/N
   
    
    xticks = np.arange(1,p_max+1)
    
    # function evaluations per step
    plt.plot(xticks,runtime, color = 'lightgreen', linestyle = 'dashed')
    
    # cummulative function evaluations
    plt.plot(xticks,cum_time, color = 'navajowhite', linestyle = 'dashed')
    
    plt.grid('on')
    plt.ylabel(r'$t$ [s]')
    plt.xlabel('p')
    plt.xlim([0.8,p_max+0.2])
  

from scipy import optimize
def test_func(x, a,b):
    return a*np.exp(np.sqrt(b*x))

# mean, including a fit
params, params_covariance = optimize.curve_fit(test_func, xticks, mean_runtime,
                                                p0=[1,1])
# error mean per step fit
perr = np.sqrt(np.diag(params_covariance))
print('mean', params, perr)

# cum, including a fit
params2, params_covariance2 = optimize.curve_fit(test_func, xticks, mean_cum_time,
                                                p0=[1, 1])
# error mean per step fit
perr2 = np.sqrt(np.diag(params_covariance2))
print('cum', params2, perr2)

plt.plot(xticks,mean_runtime, linestyle = 'None', color = 'blue', marker = 'o', label = 'runtime per step (average)')

plt.plot(xticks,mean_cum_time, linestyle = 'None', color = 'red', marker = 'o', label = 'cummulative runtime (average)')

plt.plot(xticks,test_func(xticks,params[0],params[1]), color = 'blue', linestyle = 'dashed', label = r'$a_0e^{\sqrt{p/p_0}}$')
plt.plot(xticks,test_func(xticks,params2[0],params2[1]), color = 'red', linestyle = 'dashed', label = r'$a_1e^{\sqrt{p/p_1}}$')



plt.legend()
plt.show()