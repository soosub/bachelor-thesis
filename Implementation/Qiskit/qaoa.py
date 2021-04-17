# -*- coding: utf-8 -*-
"""
Created on Sun Apr 26 16:29:26 2020

Used https://github.com/Qiskit/qiskit-aqua#Optimization as example

@author: joost
"""

# Imports - own scripts
import sys
sys.path.insert(0,'..') # adding parent folder to path
import my_graphs

# Imports - useful additional packages 
import networkx as nx
from docplex.mp.model import Model

# Imports - Qiskit
from qiskit import Aer
from qiskit.aqua import QuantumInstance
from qiskit.aqua.algorithms import QAOA
from qiskit.aqua.components.optimizers import SPSA, NELDER_MEAD
# Optimizers available: ['Optimizer', 'ADAM', 'AQGD', 'CG', 'COBYLA', 'GSLS', 'L_BFGS_B', 'NELDER_MEAD', 'NFT', 'P_BFGS', 'POWELL', 'SLSQP', 'SPSA', 'TNC', 'CRS', 'DIRECT_L', 'DIRECT_L_RAND', 'ESCH', 'ISRES']
from qiskit.optimization.applications.ising import docplex, max_cut
from qiskit.optimization.applications.ising.common import sample_most_likely

# Generate a graph and its corresponding adjacency matrix
G = nx.random_regular_graph(2,6)
n = len(G)
pos = nx.spring_layout(G)

w = my_graphs.adjacency_matrix(G) 
print("\nAdjacency matrix\n", w, "\n")

# setting p
p = 1

# ... QAOA ...
# Create an Ising Hamiltonian with docplex.
mdl = Model(name='max_cut')
mdl.node_vars = mdl.binary_var_list(list(range(n)), name='node')
maxcut_func = mdl.sum(w[i, j] * mdl.node_vars[i] * (1 - mdl.node_vars[j])
                      for i in range(n) for j in range(n))
mdl.maximize(maxcut_func)
qubit_op, offset = docplex.get_operator(mdl)

# Run quantum algorithm QAOA on qasm simulator
optimizer = NELDER_MEAD()
qaoa = QAOA(qubit_op, optimizer, p=p)
backend = Aer.get_backend('qasm_simulator')
quantum_instance = QuantumInstance(backend, shots=1000)
result = qaoa.run(quantum_instance)

x = sample_most_likely(result.eigenstate)
print('energy:', result.eigenvalue.real)
print('time:', result.optimizer_time, 's')
print('max-cut objective:', result.eigenvalue.real + offset)
print('solution:', max_cut.get_graph_solution(x))
print('solution objective:', max_cut.max_cut_value(x, w))
print('angles:', result.optimal_point)