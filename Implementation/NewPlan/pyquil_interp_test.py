# -*- coding: utf-8 -*-
"""
Created on Thu Jun  4 10:49:10 2020

@author: joost
"""

# imports
from grove.pyqaoa.qaoa import QAOA

import pyquil.api as api
import hamiltonians
from pyquil_base import counter_histogram
import matplotlib.pyplot as plt
import numpy as np
import networkx as nx


# function for determining next angles
def next_angles(angles):
    '''Takes in a set of p angles and returns a new set of p+1 angles using the INTERP method'''
    p = len(angles)
    
    new_angles = [angles[0]] # i = 1, the first angles coincide
    for i in range(2, p+1):
        new_angles.append( (i-1)/p*angles[i-2] + (p-i+1)/p*angles[i-1]) # i in {2, ... , p}, interpolation 
    new_angles.append(angles[-1]) # i = p+1, the last angles coincide
        
    return new_angles

# timing start
import time
start = time.time()

# close all earlier figures
plt.close('all')

# setting up connection with the QVM
qvm_connection = api.QVMConnection()

# constructing graph, setting p and the desired number of samples
G = nx.random_regular_graph(4,7)
qubits = [int(n) for n in list(G.nodes)]
p = 1
n_samples = 1024
        
# constructing cost and mixer hamiltonian elements in list
# N.B. This algorithm only works if all the terms in the cost Hamiltonian commute with each other.
Hc = hamiltonians.cost(G)
Hb = hamiltonians.mixer(G)

# setting up the QAOA circuit
initial_betas = 0.8
initial_gammas = 0.35 
minimizer_kwargs = {'method': 'BFGS', 'options': {'ftol': 1.0e-2, 'xtol': 1.0e-2,'disp': False}}

if type(initial_betas) == float:
    p_start = 1
else:
    p_start = len(initial_betas)
    
for i in range(p_start, p+1):
    QAOA_inst = QAOA(qvm_connection, qubits, steps=i, 
                         cost_ham = Hc,
                         ref_ham= Hb, 
                         init_betas=initial_betas,
                         init_gammas=initial_gammas,
                         minimizer_kwargs=minimizer_kwargs)
    
    # calculating angles using VQE (simulation)
    betas, gammas = QAOA_inst.get_angles()
    print(" p =",i)
    print("Values of betas:", betas)
    print("Values of gammas:", gammas, '\n')
    
    # setting next angles
    initial_betas = next_angles(betas)
    initial_gammas = next_angles(gammas)
    
    print("Values of betas ansatz:", initial_betas)
    print("Values of gammas ansatz:", initial_gammas, '\n')
    
    

# resulting bitstrings and the most common one
print("\nAnd the most common measurement is... ")
most_common_bitstring, results_counter = QAOA_inst.get_string(betas, gammas, samples=n_samples)

print(most_common_bitstring)
print(tuple(qubits))

# graphing distribution
counter_histogram(results_counter, title = " p = "+str(p))

# timing final
end = time.time()
print("Time ", end-start)