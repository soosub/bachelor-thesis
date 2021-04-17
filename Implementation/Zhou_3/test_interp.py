# -*- coding: utf-8 -*-
"""
Created on Fri Jun 26 16:21:01 2020

@author: joost
"""

import matplotlib.pyplot as plt
import networkx as nx
from INTERP import INTERP
from QAOA import QAOA
import numpy as np

G = nx.random_regular_graph(3,14, seed=1)
inti = INTERP(G, optimizer = 'Nelder-Mead', optimizer_options = {'disp':True})

p_min, p_max = 2,10

g,b = inti.get_angles_INTERP(p_max, initial_gamma = [0.35], initial_beta = [0.8])


for i in range(p_min,p_max+1):
    gamma = inti.gammas_list[i-1]
    beta = inti.betas_list[i-1]
    
    print(gamma, beta)
    
    counts = inti.sample(gamma,beta,  n_samples = 1024)
    v_counts = inti.counts_to_valueCounts(counts, plot_histogram=True)
    mean = QAOA.mean_valueCounts(v_counts)
    plt.title('Distribution objective values, p = '+str(i)+", mean = %.2f" % (mean) )
    
    plt.figure()
    plt.title(r'Pattern $\vec{\gamma}, \vec{\beta}$, p = '+str(i))
    plt.plot(np.arange(1,i+1),gamma)
    plt.plot(np.arange(1,i+1),beta)
    plt.legend([r"$\gamma_i$", r'$\beta_i$'])
    
    
    
    