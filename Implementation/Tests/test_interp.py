# -*- coding: utf-8 -*-
"""
Created on Thu Jun  4 10:24:20 2020

@author: joost
"""

from QAOA_INTERP import INTERP
import qiskit
from my_graphs import diamond
from time import time 

t_start = time()

G = diamond()
backend = qiskit.Aer.get_backend('qasm_simulator')
p = 3

g,b = INTERP.get_angles_INTERP(G, p, backend)

INTERP.sample(G, g, b, backend, plot_histogram=True)

t_end = time()

print("Time: ",t_end - t_start, "s" )