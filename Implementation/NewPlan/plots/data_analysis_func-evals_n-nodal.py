# -*- coding: utf-8 -*-
"""
Created on Fri Jul  3 08:26:06 2020

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
n = 16
pre = "data_trim/data_trim_3-regular_"
post =".csv"
filename = "unweighted_INT_"+str(n)
df = load_csv(pre+filename+post); # eine keer

# exponent or exponent of square root
SQR = True

p_max = int(np.max(df['p']))
N = len(set(df['seed']))

mean_n_evals = np.zeros(p_max)
mean_cum_evals = np.zeros(p_max)



# df.loc[df['p'] == 10][['gammas']] - Wybe
for i in range(0,len(df),p_max): 
    n_evals = np.array([df['n_Fp_evals'][i+j] for j in range(p_max)])
    cum_evals= np.array([np.sum([df['n_Fp_evals'][i+j] for j in range(k+1)]) for k in range(p_max)])
    
    mean_n_evals += n_evals/N
    mean_cum_evals += cum_evals/N
   
    
    xticks = np.arange(1,p_max+1)
    
    # function evaluations per step
    plt.plot(xticks,n_evals, color = 'lightgreen', linestyle = 'dashed')
    
    # cummulative function evaluations
    plt.plot(xticks,cum_evals, color = 'navajowhite', linestyle = 'dashed')
    
    plt.grid('on')
    plt.ylabel(r'function evaluations')
    plt.xlabel('p')
    plt.xlim([0.8,p_max+0.2])
  

from scipy import optimize
def test_func1(x, b,c):
    return b*x + c

def test_func2(x, a, b):
    return a * x**2 + b*x

# mean, including a fit
params, params_covariance = optimize.curve_fit(test_func1, xticks, mean_n_evals,
                                                p0=[1,1])
# error mean per step fit
perr = np.sqrt(np.diag(params_covariance))
print('mean', params, perr)

# cum, including a fit
params2, params_covariance2 = optimize.curve_fit(test_func2, xticks, cum_evals,
                                                p0=[1, 1])
# error mean per step fit
perr2 = np.sqrt(np.diag(params_covariance2))
print('cum', params2, perr2)

plt.plot(xticks,mean_n_evals, linestyle = 'None', color = 'blue', marker = 'o', label = 'evaluations per step (average)')

plt.plot(xticks,cum_evals, linestyle = 'None', color = 'red', marker = 'o', label = 'cummulative evaluations (average)')

plt.plot(xticks,test_func1(xticks,params[0],params[1]), color = 'blue', linestyle = 'dashed', label = r'$b_0x + c$')
plt.plot(xticks,test_func2(xticks,params2[0],params2[1]), color = 'red', linestyle = 'dashed', label = r'$a_1x^2 + b_1x$')




plt.legend()
plt.show()

