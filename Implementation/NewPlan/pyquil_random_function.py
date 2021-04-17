# -*- coding: utf-8 -*-
"""
Created on Thu Jun  4 10:49:10 2020

@author: joost
"""

# imports
from grove.pyqaoa.qaoa import QAOA
import pyquil.api as api
import hamiltonians
import networkx as nx
import time

from pyquil_base import objective_value, cutvalue_best, cutvalue_most_sampled, counter_histogram

    
def random_pyquil(G, p , initial_betas = 0.8, initial_gammas = 0.35, 
                  minimizer_kwargs = {'method': 'BFGS', 'options': {'ftol': 1.0e-2, 'xtol': 1.0e-2,'disp': True}}, 
                  n_samples = 1024, plot_hist = False):
    # timing start
    start = time.time()
    
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
    
    # saving data from all layers
    results = {}
    
    # Entering Loop
    if type(initial_betas) == float:
        p_start = 1
    else:
        p_start = len(initial_betas)
        
    for i in range(p_start, p+1):
        QAOA_inst = QAOA(qvm_connection, qubits, steps=i, 
                             cost_ham = Hc,
                             ref_ham= Hb, 
                             minimizer_kwargs=minimizer_kwargs,
                             vqe_options = {'disp': print, 'return_all': True})
        
        # calculating angles using VQE (simulation)
        print(" p =",i)
        betas, gammas = QAOA_inst.get_angles()
        print("Values of betas:", betas)
        print("Values of gammas:", gammas, '\n')
        
        # resulting bitstrings and the most common one
        print("\nAnd the most common measurement is... ")
        most_common_bitstring, results_counter = QAOA_inst.get_string(betas, gammas, samples=n_samples)
        
        print(most_common_bitstring)
        print(tuple(qubits))
        
        # graphing distribution
        if plot_hist:
            counter_histogram(results_counter, title = " p = "+str(p))
        
        # timing final
        end = time.time()
        print("Time ", end-start)
        
        # saving data from this layer
        results_i = {}
        results_i['p'] = i
        results_i['time'] = end-start
        results_i['graph'] = nx.to_dict_of_dicts(G)
        results_i['n_nodes'] = len(G.nodes)
        results_i['n_edges'] = len(G.edges)
        results_i['most_common_bistring'] = most_common_bitstring
        results_i['qubit_order'] = tuple(qubits)
        results_i['counter'] = dict(results_counter)
        results_i['n_Fp_evals'] = len(QAOA_inst.result['expectation_vals'])
        results_i['n_samples'] = n_samples
        results_i['Fp'] = -QAOA_inst.result['fun']
        results_i['Fp_sampled'] = sum([objective_value(G,k,qubits)*v for k,v in results_counter.items()])/n_samples
        results_i['cutvalue_best'] = cutvalue_best(G, results_counter, qubits)
        results_i['cutvalue_most_sampled'] = cutvalue_most_sampled(G, results_counter, qubits)
        results_i['minimizer_method'] = minimizer_kwargs['method']
        
        # time symmetry
        if all(gammas>0) and all(betas>0):
            results_i['gammas'] = gammas.copy()
            results_i['betas'] = betas.copy()
        else:
            results_i['gammas'] = -gammas.copy()
            results_i['betas'] = -betas.copy()
        
        results[i] = results_i
        
    return results