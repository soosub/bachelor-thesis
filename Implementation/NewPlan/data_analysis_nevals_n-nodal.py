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
filename = "data/data_ER-075_unweighted_INT_15.csv"
df = load_csv(filename); # eine keer


p_max = 8 #int(np.max(df['p']))
seed_max = 10
N = seed_max

mean_n_evals = np.zeros(p_max)
mean_cum_n_evals = np.zeros(p_max)

attr = 'n_Fp_evals'

df_new = df[(df['n_nodes'] == n) & (df['seed'] < seed_max) & (df['p'] <= p_max)][attr].iloc()

# df.loc[df['p'] == 10][['gammas']] - Wybe
for i in range(0,seed_max*p_max,p_max):
    n_evals = np.array([df_new[i+j] for j in range(p_max)])
    cum_n_evals = np.array([np.sum(n_evals[:k+1]) for k in range(p_max)])
    
    mean_n_evals += n_evals/N
    mean_cum_n_evals += cum_n_evals/N
   
    
    xticks = np.arange(1,p_max+1)
    
    # function evaluations per step
    plt.plot(xticks,n_evals, color = 'lightgreen', linestyle = 'dashed')
    
    # cummulative function evaluations
    plt.plot(xticks,cum_n_evals, color = 'navajowhite', linestyle = 'dashed')
    
    plt.grid('on')
    plt.ylabel(r'number of function evaluations')
    plt.xlabel('p')
    plt.xlim([0.8,p_max+0.2])
  

from scipy import optimize
def test_func1(x, b):
    return b*x

def test_func2(x, a,b):
    return a*x**2 + b*x

# mean, including a fit
params, params_covariance = optimize.curve_fit(test_func1, xticks, mean_n_evals,
                                                p0=[1])
# error mean per step fit
perr = np.sqrt(np.diag(params_covariance))
print('mean', params, perr)

# cum, including a fit
params2, params_covariance2 = optimize.curve_fit(test_func2, xticks, mean_cum_n_evals,
                                                p0=[1, 1])
# error mean per step fit
perr2 = np.sqrt(np.diag(params_covariance2))
print('cum', params2, perr2)

plt.plot(xticks,mean_n_evals, linestyle = 'None', color = 'blue', marker = 'o', label = '$F_p$ evaluations per step (average)')

plt.plot(xticks,mean_cum_n_evals, linestyle = 'None', color = 'red', marker = 'o', label = 'cummulative $F_p$ evaluations (average)')

plt.plot(xticks,test_func1(xticks,params[0]), color = 'blue', linestyle = 'dashed', label = r'$b_0p$')
plt.plot(xticks,test_func2(xticks,params2[0],params2[1]), color = 'red', linestyle = 'dashed', label = r'$a_1p^2 + b_1p$')


plt.legend()
plt.show()