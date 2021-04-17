# -*- coding: utf-8 -*-
"""
Created on Sun Jun 28 19:20:04 2020

@author: joost
"""

from pyquil_interp_function import interp_pyquil
import pandas as pd
import networkx as nx


p_max = 10 # maxdepth
N = 20 # number of graphs per node number n
d = 3 # degree of regular graphs

# creating dataframe
output = pd.DataFrame()

for n in [14,16,18,20]:
    for s in range(N+1):
        G = nx.random_regular_graph(d,n,seed=s)
        graph_type = str(d)+'-regular_'+str(n)+'-nodal'
                
        results = interp_pyquil(G,p_max)
        
        for i, results_i in results.items():
            results_i['graph_name'] = graph_type
            results_i['seed'] = s
            output = output.append(results_i, ignore_index=True)
    
        # saving every round so the process can be stopped prematurely without losing all progress
        filename = 'data_3-regular_koen.csv'
        output.to_csv(filename)

