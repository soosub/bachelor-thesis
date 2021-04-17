# -*- coding: utf-8 -*-
"""
Created on Thu Jul  2 13:37:11 2020

@author: joost
"""

from hamiltonians import cost,mixer
import networkx as nx
import pyquil.latex
import pyquil.api as api
from grove.pyqaoa.qaoa import QAOA

G = nx.random_regular_graph(2,3)

Hc = cost(G)
Hb = mixer(G)

qvm_connection = api.QVMConnection()
qubits = [int(n) for n in list(G.nodes)]

Q = QAOA(qvm_connection, qubits, steps=2, 
                             cost_ham = Hc,
                             ref_ham= Hb)

params = [3,7,2,5] # b1, b2, g1, g2 
prog = Q.get_parameterized_program()
circuit = prog(params)

# print to latex doc
s = pyquil.latex.to_latex(circuit)
print(s)

# python figure
#pyquil.latex.display(circuit) # Does not work for some reason