# -*- coding: utf-8 -*-
"""
Created on Wed Jul  1 13:13:02 2020

@author: joost
"""

from data_load import load_csv
import numpy as np
import networkx as nx
from pyquil_interp_function import brute_force
import matplotlib.pyplot as plt

folder = 'data/'
df_u3R = load_csv(folder+'data_3-regular_unweighted_INT_14.csv', True)
df_w3R = load_csv(folder+'data_3-regular_weighted_INT_14-16.csv', True)


# trimming data
last_graph = 200
u3R = df_u3R[df_u3R['n_nodes']==14][:last_graph].iloc()
w3R = df_w3R[df_w3R['n_nodes']==14][:last_graph].iloc()


p_max = 10
for df in [w3R]:
    plt.figure()
    r_sum = np.zeros(p_max)
    label = True
    for i in range(0,last_graph,p_max): 
        print("graph", i,"/",last_graph)
        Fp = [df[i+j]['Fp'] for j in range(p_max)]
        G = nx.from_dict_of_dicts(df[i]['graph'])
        Cmax = brute_force(G)
        
        r = np.array([Fp[i]/Cmax for i in range(p_max)])
        r_sum += r
        
        pticks = np.arange(1,p_max+1)
        
        #plt.title(r"$F_p$ for 12-nodal 3-regular graphs for $p = 1...10$")
        plt.yscale("log")
        if label:
            plt.plot(pticks,1-r, color = 'peachpuff', linestyle = 'dashed')
            plt.plot(pticks,1-r, color = 'darkorange', linestyle = 'None', marker = 'o', label = 'random instance')
            label = False
        else:
            plt.plot(pticks,1-r, color = 'peachpuff', linestyle = 'dashed')
            plt.plot(pticks,1-r, color = 'darkorange', linestyle = 'None', marker = 'o')
        plt.grid(True,which="both", ls="-")
        plt.ylabel(r'$1-r$')
        plt.xlabel('p')
       
    # Mean, including a fit
    from scipy import optimize
    def test_func(p, a, b):
        return a * np.exp(-np.sqrt(p / b))
    
    
    r_mean = r_sum/len(range(0,last_graph,p_max))
    params, params_covariance = optimize.curve_fit(test_func, pticks, 1-r_mean,
                                                   p0=[0.8, 2])
        
    plt.plot(pticks,1-r_mean, color = 'maroon', linestyle = 'None', marker = 'o', label = 'mean')
    plt.plot(pticks,test_func(pticks,params[0],params[1]), color = 'firebrick', linestyle = 'dashed', label = r'$\alpha e^{-\sqrt{p/p_0}}$')
    
    plt.legend()
    plt.show()