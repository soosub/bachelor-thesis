# -*- coding: utf-8 -*-
"""
Created on Mon Apr 27 14:58:45 2020

@author: joost

Used https://github.com/mstechly/quantum_tsp_tutorials/blob/master/tutorials/02_QAOA.ipynb as example
"""
# imports
from grove.pyqaoa.qaoa import QAOA

import pyquil.api as api
import my_graphs
import hamiltonians
import results
import matplotlib.pyplot as plt

#timing start
import time
start = time.time()

# setting up connection with the QVM
qvm_connection = api.QVMConnection()

# constructing graph, setting p and the desired number of samples
G = my_graphs.diamond()
qubits = [int(n) for n in list(G.nodes)]
p = 1
n_samples = 1024
        
# constructing cost and mixer hamiltonian elements in list
# N.B. This algorithm only works if all the terms in the cost Hamiltonian commute with each other.
Hc = hamiltonians.cost(G)
Hb = hamiltonians.mixer(G)

# setting up the QAOA circuit
initial_beta = 0 # [1.4602835,  2.29429135, 1.12184905, 0.36504919, 0.15778852]
initial_gamma = 0 # [0.23854042, 3.22162263, 5.20630089, 0, 2.62449872]
minimizer_kwargs = {'method': 'BFGS', 'options': {'ftol': 1.0e-2, 'xtol': 1.0e-2,'disp': True}}

QAOA_inst = QAOA(qvm_connection, qubits, steps=p, 
                     cost_ham = Hc,
                     ref_ham= Hb, 
                     init_betas=initial_beta,
                     init_gammas=initial_gamma,
                     minimizer_kwargs=minimizer_kwargs)

# calculating angles using VQE (simulation)
betas, gammas = QAOA_inst.get_angles()
print("Values of betas:", betas)
print("Values of gammas:", gammas)
print()

# save circuit
import numpy as np
angles = np.hstack((betas, gammas))
param_prog = QAOA_inst.get_parameterized_program()
prog = param_prog(angles)
len_prog = len(prog)

# resulting bitstrings and the most common one
print("\nAnd the most common measurement is... ")
most_common_bitstring, results_counter = QAOA_inst.get_string(betas, gammas, samples=n_samples)

print(most_common_bitstring)
print(tuple(qubits))

# graphing distribution
results.counter_histogram(results_counter)#, title = " p = "+str(p))

# plotting cut
#my_graphs.plot_cut(G, most_common_bitstring)
print("\n(*) Drawing cut, yet to be implemented")


# timing final
end = time.time()
print("Time ", end-start)
