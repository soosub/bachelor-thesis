# -*- coding: utf-8 -*-
"""
Created on Tue Apr 28 11:43:07 2020

@author: joost
"""

from pyquil.paulis import PauliTerm, PauliSum

def cost(G):
    ''' Takes in a graph and constructs the cost Hamiltonian'''
    graph = G.copy()
    cost_operators = []
    for i, j, w in graph.edges(data=True):
        i, j = int(i), int(j) # using the right type
        if 'weight' in w:
            weight = w['weight']
        else:
            weight = 1
        cost_operators.append(0.5*weight*(PauliTerm("Z", i)*PauliTerm("Z", j) - PauliTerm("I", 0)))
        
    return cost_operators

def mixer(G):  
    ''' Takes in a graph and constructs the mixer Hamiltonian'''
    graph = G.copy()
    driver_operators = []
    for i in [int(n) for n in list(graph.nodes)]:
        i = int(i) # using the right type
        driver_operators.append(PauliSum([PauliTerm("X", i, -1.0)]))
    return driver_operators