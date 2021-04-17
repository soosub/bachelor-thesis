# -*- coding: utf-8 -*-
"""
Created on Mon Jun  1 11:38:02 2020

@author: joost
"""

import qiskit 
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import scipy

class QAOA:    
    def objective(G, x):
        '''Calculating the value of a cut x on graph G, 
        where x is represented by a numpy array of 1s and 0s
        '''        
        
        w = nx.to_numpy_array(G)
        spin = (-1)**x # bijection from 0,1 to 1,-1
        
        return 0.5*sum([w[i,j]*(1-spin[i]*spin[j]) for i,j in G.edges]) 
    
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
                circ.rz(-gamma[i]*w[a,b],b) #PLUS or MINUS! Does it matter? We optimize anyway? - it does affect the range of gamma and the patterns
                circ.cx(a,b)
            for a in G.nodes: # U(B, beta) gates for every node
                circ.rx(2*beta[i], a)
        
        circ.measure_all()
        
        return circ
    
    def expectation(G, gamma, beta, backend, n_samples = 1024):
        '''Evaluates expectation for given graph and angles'''
        
        # create circuit and run it n_samples times
        counts = QAOA.sample(G, gamma, beta, backend, n_samples = n_samples)
        
        def bitstring_to_array(x):
            return np.array([int(d) for d in str(x)])
        
        avg = sum([counts[x] * QAOA.objective(G,bitstring_to_array(x)) for x in counts])/n_samples
        
        return avg
    
    def find_local_angles(G, gamma, beta, backend, n_samples = 1024, optimizer = 'Nelder-Mead', optimizer_options = None):
        '''Find local optimum beginning from gamma, beta (these are overwritten)
        Note that (gamma,beta) is the initial point and are NOT overwritten when this method is run
        '''    
    
        def fun(angles):
            ''' The objective function to be optimised by varying the angles
            Note, we want to maximize the expectation <Hc>, this is equivalent to 
            minimizing - <Hc>'''
            new_gamma = angles[:len(angles)//2]
            new_beta = angles[len(angles)//2:]
            
            # maximize f = minimize -f 
            return -QAOA.expectation(G, new_gamma, new_beta, backend, n_samples) 
        
        x0 = gamma+beta
        result = scipy.optimize.minimize(fun, x0, method= optimizer)
        
        # finding angles
        angles = result.x
        new_gamma = angles[:len(angles)//2]
        new_beta = angles[len(angles)//2:]
        return new_gamma, new_beta
    
    def gridsearch(G, backend, n_samples=1024, 
                               n_gamma = 100, n_beta = 100,                                
                               plot_F = False, imshow_F = False, print_optimum = False,
                               g_min = 0, g_max = np.pi, b_min = 0, b_max = np.pi):
        '''Does a gridsearch to find optimal angles at p = 1, additionally it returns the landscape F
        as gamma,beta, F'''
        from tqdm import tqdm
        
        g_grid = np.linspace(g_min, g_max, n_gamma)
        b_grid = np.linspace(b_min, b_max, n_beta)
        
        F = np.zeros([len(g_grid), len(b_grid)])
        
        for i in tqdm(range(len(g_grid))):
            for j in range(len(b_grid)):
                F[i][j] = QAOA.expectation(G, [g_grid[i]], [b_grid[j]], backend, n_samples)
        
        result = np.where(F == np.amax(F))
        a      = list(zip(result[0],result[1]))[0]

        gamma_max  = g_grid[a[0]]
        beta_max   = b_grid[a[1]]
        
        if plot_F:
            # Plot the expetation value F1
            from   matplotlib import cm
            from   matplotlib.ticker import LinearLocator, FormatStrFormatter
            from math import ceil
            
            fig = plt.figure()
            ax  = fig.gca(projection='3d')
            
            g_grid, b_grid = np.meshgrid(g_grid, b_grid)
            
            F = F.transpose()
            F = np.flip(F,0)
            
            ax.plot_surface(g_grid, b_grid[::-1], F, cmap=cm.coolwarm, linewidth=0, antialiased=True)
            
            ax.set_zlim(0,ceil(np.amax(F)))
            ax.zaxis.set_major_locator(LinearLocator(3))
            ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))
            
            # Labels
            ax.set_xlabel(r'$\gamma$')
            ax.set_ylabel(r'$\beta $')
            ax.set_zlabel('$F$')
                        
            plt.show()
        
        if imshow_F:            
            fig = plt.figure()
            
            plt.imshow(F, extent = [g_min , g_max, b_min , b_max])
            plt.colorbar()
            
            # Labels
            plt.xlabel(r'$\gamma$')
            plt.ylabel(r'$\beta $')
            
            # maximum
            plt.plot([gamma_max],[beta_max],'ro')
            
        if print_optimum:
            #The smallest parameters and the expectation can be extracted
            print('\n --- OPTIMAL PARAMETERS --- \n')
            print('The maximal expectation value is:  M1 = %.03f' % np.amax(F))
            print('This is attained for gamma = %.03f and beta = %.03f' % (gamma_max,beta_max))
            
        return gamma_max, beta_max, F
                
      
    def sample(G, gamma, beta, backend, n_samples = 1024, plot_histogram = False):
        circ = QAOA.create_circuit(G,beta,gamma)
        result = qiskit.execute(circ, backend = backend, shots = n_samples).result()
        counts = result.get_counts()
        
        if plot_histogram:
            from qiskit.tools.visualization import plot_histogram
            plot_histogram(counts)
            
        return counts
    
    def draw_graph(G):
        nx.draw(G)
        raise NotImplementedError("Add labels (correctly!)")
        
    def draw_cut(G, x):
        raise NotImplementedError
    
    
    
    
        
   
    
