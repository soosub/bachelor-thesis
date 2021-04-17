# -*- coding: utf-8 -*-
"""
Created on Sat Jun 27 18:33:38 2020

@author: joost
"""

import numpy as np
import networkx as nx
from QAOA import QAOA
from my_graphs import randomize_weights

G = nx.erdos_renyi_graph(9,0.75)
G = randomize_weights(G)

q = QAOA(G,1000)

dif = []

for i in range(100):
    x = np.random.uniform()
    y = np.random.uniform()
    
    d = q.expectation([x],[y]) - q.expectation([x],[y])
    print(i, d)
    
    dif.append(d)
    
print("----------------")
print(np.average(dif))
print(np.std(dif))