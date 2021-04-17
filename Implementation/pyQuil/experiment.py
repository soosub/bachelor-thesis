# -*- coding: utf-8 -*-
"""
Created on Tue May  5 13:48:49 2020

@author: joost

Per experiment it returns a dictionary with the following keys
    - energy
    - time (in seconds)
    - iterations
    - max-cut objective
    - solution
    - solution objective

Multiple experiments are run and the data will be collected in a dataframe.
"""

# imports
from grove.pyqaoa.qaoa import QAOA
import hamiltonians

# qvm_connection = backend ??
def run_experiment(G, p, optimizer, qvm_connection, n_shots = 8192, print_result = False):
    '''Runs (pyQuil) QAOA experiment with the given parameters
    Inputs

    Returns a dictionary with the following keys (some are yet to be implemented)
    - energy
    - time (in seconds)
    - iterations
    - max-cut objective
    - solution
    - solution objective

    '''
    n = len(G)                                # number of nodes / qubits
    qubits = [int(n) for n in list(G.nodes)]  # list of qubits

    # constructing cost and mixer hamiltonian elements in list
    Hc = hamiltonians.cost(G)
    Hb = hamiltonians.mixer(G)

    # setting up the QAOA circuit
    initial_beta = 0
    initial_gamma = 0
    
    QAOA_inst = QAOA(qvm_connection, qubits, steps=p,
                         cost_ham = Hc,
                         ref_ham= Hb,
                         init_betas=initial_beta,
                         init_gammas=initial_gamma,
                         minimizer_kwargs=optimizer,
                         vqe_options = {'samples': n_shots})

    # calculating angles using VQE (simulation)
    angles = QAOA_inst.get_angles()
    betas, gammas = angles

    # resulting bitstrings and the most common one
    most_common_bitstring, results_counter = QAOA_inst.get_string(betas, gammas, samples=n_shots)
    
    # Results
    energy = None
    time = None
    iterations = None
    objective = None
    solution = most_common_bitstring
    solution_objective = None
    distribution = results_counter
    angles = angles
    
    if print_result:
        print('energy:', energy)
        print('time:', time, 's')
        print('max-cut objective:', objective)
        print('solution:', solution)
        print('solution objective:', solution_objective)
        print('anlges:', angles)
        
    return {'energy':energy, 
            'time':time, 
            'iterations': iterations,
            'max-cut objective': objective, 
            'solution': solution, 
            'solution objective': solution_objective,
            'distribution': distribution,
            'angles': angles}