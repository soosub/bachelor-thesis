# -*- coding: utf-8 -*-
"""
Created on Fri May 15 17:52:43 2020

@author: joost
"""
import networkx as nx
from QAOA import *
import qiskit
from my_graphs import *

# create nice graph
G = cycle_graph(8)
backend = qiskit.Aer.get_backend('qasm_simulator')
p = 10

g, b = get_angles_INTERP(G,p,backend)
print(g,b)

S = sample(G, g, b, backend, n_samples = 1024, plot_histogram=True)