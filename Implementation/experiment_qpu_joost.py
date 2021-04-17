import networkx as nx
from scipy.optimize import minimize
import pandas as pd

# pyquil
from pyquil import get_qc
from pyquil.paulis import PauliSum, PauliTerm

# EntropicaQAOA imports
from entropica_qaoa.qaoa.parameters import StandardParams
from entropica_qaoa.qaoa.cost_function import QAOACostFunctionOnQVM
from entropica_qaoa.utilities import hamiltonian_from_graph

# function for INTERP
def next_angles(angles):
    '''Takes in a set of p angles and returns a new set of p+1 angles using the INTERP method'''
    p = len(angles)
    
    new_angles = [angles[0]] # i = 1, the first angles coincide
    for i in range(2, p+1):
        new_angles.append( (i-1)/p*angles[i-2] + (p-i+1)/p*angles[i-1]) # i in {2, ... , p}, interpolation 
    new_angles.append(angles[-1]) # i = p+1, the last angles coincide
        
    return new_angles

# setting up graph
G = nx.random_regular_graph(3,8, seed = 1)
for i,j,w in G.edges(data=True):
    if w == {}:
        w['weight'] = 1
n_qubits = len(G)


# constructing Hamiltonian
Hi = hamiltonian_from_graph(G)
terms1 = [1/2*(PauliTerm("I",0)) for i in range(len(Hi))]
terms2 = [-1/2*Hi[i] for i in range(len(Hi))]
H = PauliSum(terms1+terms2) 

# Specify initial angles
betas = [0.35]
gammas = [0.8]

# setting up qc
qc = get_qc('Aspen-8') # setting up qc [change this]
# choose from pyquil.list_quantum_computers()

# parameters
method = "Nelder-Mead" # BFGS did not work very well when run as qvm
p_max = 5 # depends on speed [could be lower if time does not allow 5]
nshots = 100 # depends on speed [possibly needs some tweaking]

output = pd.DataFrame()

for p in range(1,p_max+1):
    print('p=',p,'/',p_max)
    if p > 1:
        betas = next_angles(betas)
        gammas = next_angles(gammas)
    
    parameters = (betas, gammas)
    params = StandardParams([H,p],parameters)
    
    # NOTE - the optimiser will reach its maximum number of iterations, but for the parameters being used here,
    # the choice maxiter=200 seems to be more than sufficient to get to the optimum with high probability.
    cost_function = QAOACostFunctionOnQVM(-1*H,params, qc, nshots = nshots)
    
    # minimizing with VQE
    res = minimize(cost_function, params.raw(),
                   tol=1e-3, method=method, options={"disp": True, "maxiter": 200})
    
    # updating gammas and betas
    params.update_from_raw(res["x"])
    betas, gammas = params.betas, params.gammas
    
    results = {'p':p, 'betas':betas, 'gammas':gammas}
    results.update(dict(res))
    
    output = output.append(results, ignore_index=True) # corrected dictionary to results
    output.to_csv('experiment_qpu_joost.csv')
