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
from pyquil import api, get_qc
from experiment import run_experiment
import pandas as pd
import my_graphs

# setting up connection with the QVM
backend = get_qc("9q-square", as_qvm=True)
backend_name = backend.name

#qvm_connection = api.QVMConnection()



# constructing graph, setting p and the desired number of samples
graphs = {'diamond': my_graphs.diamond(), 
          'butterfly': my_graphs.butterfly(), 
          'regular(3,4)': my_graphs.random_regular(3, 4)}

# Setting p and number of repetitions per p
repetitions = 10
p_min, p_max = 1, 3

# Optimizer (minimizer_kwargs)
optimizer = {'method': 'Nelder-Mead', 'options': {'ftol': 1.0e-2, 'xtol': 1.0e-2,'disp': False}}


# Producing the data
for key, value in graphs.items():
    graph_name = key
    G = value
    qubits = [int(n) for n in list(G.nodes)]
    for p in range(p_min,p_max + 1):
        output = pd.DataFrame()
    
        # specifications
        specs = {'graph': graph_name, 'p': p, 'optimizer': optimizer['method'], 'backend': backend_name, 'noise': False}
    
        for i in range(repetitions):
            # Running an experiment
            print("\nExperiment "+str(i+1)+"/"+str(repetitions)+", p = "+str(p))
    
            result = run_experiment(G, p, optimizer, backend, print_result = True)
            result.update(specs) #adding specifications to the dictionary
    
            output = output.append(result, ignore_index=True)
    
        title = 'pyquil-'+ specs['graph'] +'-'+specs['backend']+'-noiseless-p'+str(p)
        output.to_csv('data/'+title+'.csv')
