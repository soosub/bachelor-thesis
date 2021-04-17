# -*- coding: utf-8 -*-
"""
Created on Tue Jun 30 13:40:22 2020

@author: joost
"""

from pyquil_interp_function import interp_pyquil
import pandas as pd
import networkx as nx
from data_load import load_csv
from GW import goemans_williamson 

# creating dataframe without overwriting (so additing)
# if you start a new set of data, make sure you start with a fresh file
filename = 'data_2-regular.csv'
overwrite = False

if overwrite == True:
    output = pd.DataFrame()
else:
    output = load_csv(filename)

p_max = 10 # maxdepth
n_min, n_max = 3, 20
N = 1 # number of graphs per node number n
d = 2 # degree of regular graphs

for n in range(n_min, n_max+1):
    for s in range(1,N+1):
        G = nx.cycle_graph(n)
        graph_type = str(d)+'-regular_'+str(n)+'-nodal'
                
        results = interp_pyquil(G,p_max)
        
        for i, results_i in results.items():
            results_i['graph_name'] = graph_type
            results_i['seed'] = s
            results_i['GW_cutvalue'] = goemans_williamson (G)
            output = output.append(results_i, ignore_index=True)
    
        # saving every round so the process can be stopped prematurely without losing all progress
        output.to_csv(filename)