# -*- coding: utf-8 -*-
"""
Created on Sun Jun 28 19:20:04 2020

@author: joost
"""

from pyquil_interp_function import interp_pyquil, brute_force
import pandas as pd
import networkx as nx
from GW import goemans_williamson as gw
import numpy as np
import time


p_max = 8 # maxdepth
N = 20 # number of graphs per node number n
d = 3 # degree of regular graphs
n_gw = 10 # number of tries GW algorithm per graph

# creating dataframe
filename = 'data_3-regular_koen2.csv'
output = pd.DataFrame()

for n in [8,10,12,14,16,18,20]: # 12 en 14 zijn gedaan, maar wss duurt dit niet heel lang en is wel makkelijker om het in een bestand te hebben
    for s in range(N+1):
        G = nx.random_regular_graph(d,n,seed=s)
        graph_type = str(d)+'-regular_'+str(n)+'-nodal'
           
        # GW tries
        gw_samples = [gw(G) for _ in range(n_gw)]
        gw_mean = np.mean(gw_samples)
        gw_std = np.std(gw_samples)
        gw_max = np.max(gw_samples)
        gw_min = np.min(gw_samples)
        print("GW mean =", gw_mean)
                
        # Cmax (optimal)
        start_brute = time.time()
        Cmax = brute_force(G)
        gw_bound = 0.878 * Cmax
        end_brute = time.time()
        brute_time = end_brute - start_brute
        print("Cmax =",Cmax)
        
        # INTERP
        results = interp_pyquil(G,p_max)        
        
        # Writing to file
        for i, results_i in results.items():
            results_i['GW_samples'] = gw_samples
            results_i['GW_mean'] = gw_mean
            results_i['GW_std'] = gw_std
            results_i['GW_max'] = gw_max
            results_i['GW_min'] = gw_min
            results_i['GW_bound'] = gw_bound
            results_i['Cmax'] = Cmax
            results_i['brute_time'] = brute_time
            results_i['graph_name'] = graph_type
            results_i['seed'] = s
            output = output.append(results_i, ignore_index=True)
    
        # saving every round so the process can be stopped prematurely without losing all progress
        output.to_csv(filename)

