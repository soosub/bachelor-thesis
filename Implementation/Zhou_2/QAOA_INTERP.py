# -*- coding: utf-8 -*-
"""
Created on Mon Jun  1 11:47:35 2020

@author: joost
"""
from QAOA import QAOA

class INTERP(QAOA):
    
    def get_angles_INTERP(G, p, backend, initial_gamma = [0.8], initial_beta = [0.35]):
        '''
        Finds quasi-optimal angles for a given graph G
        Iteratively increase p, using an interpolation-based strategy
        to find initial points for optimization
        '''
        assert len(initial_gamma) == len(initial_beta), "Angle arrays must be of the same length"
        
        def INTERP_next_angles(angles):
            '''Takes in a set of p angles and returns a new set of p+1 angles using the INTERP method'''
            
            assert len(gamma) == len(beta), "Both lists of parameters gamma, beta must be of the same length"
            
            p = len(angles)
            
            new_angles = [angles[0]] # i = 1, the first angles coincide
            for i in range(2, p+1):
                new_angles.append( (i-1)/p*angles[i-2] + (p-i+1)/p*angles[i-1]) # i in {2, ... , p}, interpolation 
            new_angles.append(angles[-1]) # i = p+1, the last angles coincide
                
            return new_angles
    
        # find first set of angles
        gamma,beta = QAOA.find_local_angles(G,initial_gamma,initial_beta,backend)
        
        for i in range(p-len(initial_gamma)):
            gamma_ansatz,beta_ansatz = INTERP_next_angles(gamma), INTERP_next_angles(beta) # new initial points
            print("ansatz gamma, beta", gamma_ansatz, beta_ansatz)
            gamma,beta = QAOA.find_local_angles(G,gamma_ansatz,beta_ansatz,backend) # new (local) optima  
            print("local optima", gamma, beta)
        
        return gamma, beta
    