# -*- coding: utf-8 -*-
"""
Created on Tue May  5 13:31:53 2020

@author: joost

Turned the qaoa.py file into a function, in order to run experiments with more ease
"""

# Imports - own scripts
from my_graphs import adjacency_matrix

# Imports - useful additional packages 
from docplex.mp.model import Model

# Imports - Qiskit
from qiskit.aqua import QuantumInstance
from qiskit.aqua.algorithms import QAOA
from qiskit.optimization.applications.ising import docplex, max_cut
from qiskit.optimization.applications.ising.common import sample_most_likely

# Runs a experiment
def run_experiment(G, p, optimizer, backend, 
                   n_shots = 100, #important for running time, max is 8192
                   print_result = False, 
                   skip_qobj_validation=False,
                   noise_model = None,
                   coupling_map = None,
                   basis_gates = None,
                   ):
    '''Runs (Qiskit) QAOA experiment with the given parameters
    Inputs
    - G, graph
    - p, number of angles
    - optimizer, classical optimizer
    - backend
    - number of shots (n_shots) - Note, this parameter is important for running time but also affects accuracy if too low
    - ...
    
    Returns a dictionary with the following keys
    - energy
    - time (in seconds)
    - iterations
    - max-cut objective
    - solution
    - solution objective
    - eigenstate distribution
    - angles
    
    '''
    
    n = len(G)                          # number of nodes
    w = adjacency_matrix(G)             # calculating adjacency matrix from graph
    
    # ... QAOA ...
    # Create an Ising Hamiltonian with docplex.
    mdl = Model(name='max_cut')
    mdl.node_vars = mdl.binary_var_list(list(range(n)), name='node')
    maxcut_func = mdl.sum(w[i, j] * mdl.node_vars[i] * (1 - mdl.node_vars[j])
                          for i in range(n) for j in range(n))
    mdl.maximize(maxcut_func)
    qubit_op, offset = docplex.get_operator(mdl)
    
    # Construct a circuit from the model
    qaoa = QAOA(qubit_op, optimizer, p=p)
    quantum_instance = QuantumInstance(backend, shots= n_shots, 
                                       skip_qobj_validation=skip_qobj_validation,
                                       coupling_map = coupling_map,
                                       basis_gates = basis_gates,
                                       noise_model = noise_model)
    
    
    # Run quantum algorithm QAOA on the backend
    result = qaoa.run(quantum_instance)
    x = sample_most_likely(result.eigenstate)
    
    # Results
    energy = result.eigenvalue.real
    time = result.optimizer_time
    iterations = result.optimizer_evals
    objective = result.eigenvalue.real + offset # why offset?
    solution = max_cut.get_graph_solution(x)
    solution_objective = max_cut.max_cut_value(x, w)
    distribution = result.eigenstate
    angles = result.optimal_point
    
    if print_result:
        print('energy:', energy)
        print('time:', time, 's')
        print('max-cut objective:', objective)
        print('solution:', solution)
        print('solution objective:', solution_objective)
        print('angles:', angles)
        
    return {'energy':energy, 
            'time':time, 
            'iterations': iterations,
            'max-cut objective': objective, 
            'solution': solution, 
            'solution objective': solution_objective,
            'distribution': distribution,
            'angles': angles,
            'n_shots': n_shots}
    