# -*- coding: utf-8 -*-
"""
Created on Tue Jun 23 10:21:24 2020

@author: joost
"""

from QAOA import QAOA
from pyswarm import pso
import numpy as np


class PSO(QAOA):
    
    def get_angles_PSO(G, p, backend, n_samples = 1024, maxiter = 50, debug = False):
        '''
        Finds angles for a given graph G using particle swarm optimization
        '''
        
        def func(x):
            '''function to be optimized'''
            g = x[::2]
            b = x[1::2]
            return -QAOA.expectation(G,g,b,backend, n_samples)
    
        # g is the first index, b is the latter
        lb = [0,0]*p
        ub = [np.pi/2, np.pi/4]*p
        xopt, fopt = pso(func, lb, ub, maxiter = maxiter,debug = debug)
        
        print(fopt)
        
        gamma = xopt[::2]
        beta = xopt[1::2]
        return gamma, beta
    
    
    