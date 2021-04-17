# -*- coding: utf-8 -*-
"""
Created on Tue Jun 23 10:21:24 2020

@author: joost
"""

from QAOA import QAOA
from pyswarm import pso
import numpy as np


class PSO(QAOA):
    def get_angles_PSO(self, p, maxiter = 10, debug = False,
                       g_min = 0, g_max = np.pi/2,
                       b_min = 0, b_max = np.pi/4,
                       swarmsize = 100):
        '''
        Finds angles for a given graph G using particle swarm optimization
        '''
        
        def func(x):
            '''function to be optimized'''
            g = x[:len(x)//2]
            b = x[len(x)//2:]
            return -self.expectation(g,b)
    
        # g is the first index, b is the latter
        lb = [g_min]*p+[b_min]*p
        ub = [g_max]*p+[b_max]*p
        xopt, fopt = pso(func, lb, ub, maxiter = maxiter,debug = debug, swarmsize=swarmsize)
        
        print(fopt)
        
        gamma = xopt[:len(xopt)//2]
        beta = xopt[len(xopt)//2:]
        return gamma, beta
    
    
    