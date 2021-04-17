# -*- coding: utf-8 -*-
"""
Created on Fri Jun  5 11:17:44 2020

@author: joost
"""
import networkx as nx
import qiskit
from qiskit import *
import my_graphs

def create_circuit(G, gamma, beta):
    '''Creating QAOA circuit for given angles'''
    # Setting p (and checking if beta and gamma are of the same size)
    if len(beta) == len(gamma):
        p = len(beta)
    else:
        raise ValueError("The parameter array beta must have the same length as parameter gamma")
    
    w = nx.to_numpy_array(G) # weights
    
    n = len(G)
    circ = qiskit.QuantumCircuit(n)
    
    for i in range(n): # superposition state using hadamards
        circ.h(i)
        
    for i in range(p): 
        for a,b in G.edges: # U(C,gamma) gates for every edge
            circ.cx(a,b)
            circ.rz(gamma[i]*w[a,b],b) #PLUS or MINUS! Does it matter? We optimize anyway - it does affect the range of gamma and the patterns
            circ.cx(a,b)
        for a in G.nodes: # U(B, beta) gates for every node
            circ.rx(2*beta[i], a)
    
    circ.measure_all()
    
    return circ

IBMQ.load_account()
provider = IBMQ.get_provider(hub='ibm-q')
provider.backends()

# setting backend
backend = provider.get_backend('ibmq_qasm_simulator')

# creating circuit
gamma, beta = [1],[1]
G = my_graphs.diamond()
qc = create_circuit(G, gamma, beta)

print('starting job')
job = execute(qc, backend, shots=1024)
print('finished job')

result = job.result().get_counts()

print (result)


















