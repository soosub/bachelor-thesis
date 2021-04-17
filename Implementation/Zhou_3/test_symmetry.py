# -*- coding: utf-8 -*-
"""
Created on Sat Jun 27 18:20:55 2020

@author: joost
"""
import numpy as np
import networkx as nx
from QAOA import QAOA
import matplotlib.pyplot as plt

G = nx.erdos_renyi_graph(13,0.1)
q = QAOA(G,n_samples = 10000)

dif = []

for i in range(100):
    x1 = np.random.uniform(0,100) # gamma
    y1 = np.random.uniform(0,100) # beta
    
    x2, y2 = QAOA.remove_degeneracies(x1,y1)
    
    print("deg", x1, y1, 0 < x1< np.pi/2, 0 < y1 < np.pi)
    print("undeg", x2, y2, 0 < x2< np.pi/2, 0 < y2 < np.pi)
    
    d = q.expectation([x1],[y1]) - q.expectation([x2],[y2])
    print(i, d)
    
    dif.append(d)
    
print("----------------")
print(np.average(dif))
print(np.std(dif))

plt.hist(dif)