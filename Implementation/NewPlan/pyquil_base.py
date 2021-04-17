# -*- coding: utf-8 -*-
"""
Created on Thu Jul  2 16:39:22 2020

@author: joost
"""

import hamiltonians
import pyquil.api as api
from grove.pyqaoa.qaoa import QAOA
import numpy as np
import itertools
import matplotlib.pyplot as plt
import collections

def construct_QAOA(G,p, 
                   minimizer_kwargs= {'method': 'BFGS', 'options': {'ftol': 1.0e-2, 'xtol': 1.0e-2,'disp': True}},
                   init_betas=None,
                   init_gammas=None,
                   vqe_options = {'disp': print, 'return_all': True}):
    # setting up connection with the QVM
    qvm_connection = api.QVMConnection()
    
    # labelling qubits according to graph
    qubits = [int(n) for n in list(G.nodes)]
    
    # turning unweighted graphs into weighted graph with weight wij = 1
    for (u, v) in G.edges():
        if G.edges[u,v] == {}:
            G.edges[u,v]['weight'] = 1
            
    # constructing cost and mixer hamiltonian elements in list
    # N.B. This algorithm only works if all the terms in the cost Hamiltonian commute with each other.
    Hc = hamiltonians.cost(G)
    Hb = hamiltonians.mixer(G)
    
    return QAOA(qvm_connection, qubits, steps=p, 
                             cost_ham = Hc,
                             ref_ham= Hb, 
                             minimizer_kwargs=minimizer_kwargs,
                             vqe_options = vqe_options)

def brute_force(G):
    n = len(G)
    # turning unweighted graphs into weighted graph with weight wij = 1
    for (u, v) in G.edges():
        if G.edges[u,v] == {}:
            G.edges[u,v]['weight'] = 1
    qubit_order = list(np.arange(0,n))
    return np.max([objective_value(G,np.append([0],np.array(p)),qubit_order = qubit_order) for p in itertools.product([0,1], repeat=n-1)])

def expectation(G,gammas,betas,n_samples = 100):
    '''Calculates expecation for a given set of angles, beta, gamma
    qaoa is an QAOA object from pyQuil'''
    p = len(gammas)
    q = construct_QAOA(G,p)
    _, string = q.get_string(betas,gammas,samples = n_samples)
    return np.sum([objective_value(G,k,q.qubits)*v for k,v in string.items()])/n_samples 
 
def objective_value(G,x, qubit_order):
    '''Returns objective value for a given cut, given qubit_order'''
    return sum([0.5*w['weight']*(1-(-1)**x[qubit_order.index(i)]*(-1)**x[qubit_order.index(j)]) for i,j,w in G.edges(data=True) ])
 
def cutvalue_best(G,counter, qubit_order):
    return max([objective_value(G,cut,qubit_order) for cut,count in counter.items()])

def cutvalue_most_sampled(G,counter, qubit_order):
    cut = max(counter, key=counter.get)
    return objective_value(G, cut, qubit_order)

def counter_histogram(results_counter, title=""):
    '''Creates a histogram from a Counter dictionary of results'''
    plt.figure()
    
    w = collections.Counter(results_counter)
    N = sum(w.values())
    
    plt.bar([''.join(map(str,x)) for x in w.keys()], [x/N for x in w.values()])
    plt.xlabel("state")
    plt.ylabel("probability within sample")
    plt.title(title)
    plt.show()
