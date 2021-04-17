# -*- coding: utf-8 -*-
"""
Created on Fri Jun 26 22:30:35 2020

@author: joost
"""
from PSO import PSO
import networkx as nx

G = nx.random_regular_graph(3,10, seed=1)

pso = PSO(G, n_samples = 10000)

gammas_list = []
betas_list = []
expectation_list = []

for p in [1,2,3,4,5]:
    g,b = pso.get_angles_PSO(p, debug = True, maxiter = 10, swarmsize= 50)
    
    gammas_list.append(g)
    betas_list.append(b)
    
    expectation = pso.expectation(g,b)
    expectation_list.append(expectation)
    
    print('\np='+str(p), expectation,'\n')
    

    