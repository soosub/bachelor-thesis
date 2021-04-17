# -*- coding: utf-8 -*-
"""
Created on Tue Jun 23 17:43:27 2020

@author: joost
"""

from QAOA import QAOA
import numpy as np
import scipy.optimize
from tqdm import tqdm


class FOURIER(QAOA):
            
    def get_angles_FOURIER_constant(self, p, q, R=0, initial_u = None, initial_v = None): 
        '''
        Finds quasi-optimal angles for a given graph G using the FOURIER[q=c,R] method
        where c is a constant independent from p. For the method FOURIER[q=pmR] have a look
        at the get_angles_FOURIER_infinity method.
        
        q is the number of frequency components in the ansatz for gamma, beta
        R is the number of perturbations, similar to what's done in particle swarm optimization
        
        The amplitudes of the respective frequencies are translated to angles
        '''
        if initial_u == None:
            initial_u = [0]*q
        if initial_v == None:
            initial_v = [0]*q
        
        assert len(initial_u) == len(initial_v) == q, "Initial amplitude arrays must be of the same size, namely q"        
        
        for i in tqdm(range(1,p+1)):
            u, v = self.find_local_amplitudes(initial_u, initial_v, i)            
            initial_u, initial_v = u.copy(), v.copy()
        
        return FOURIER.translate_fourier_to_angles(u, v, p)
    
    def get_angles_FOURIER_infinity(self, p, backend, R=0, initial_u = None, initial_v = None):
        print(self.n_samples)
        raise NotImplementedError
        
        def FOURIER_next_amplitudes(amplitudes):
            '''Takes in a set of amplitudes and returns a new set of amplitudes using the FOURIER(q,R) method'''
            return amplitudes+[0]
    
    def translate_fourier_to_angles(u, v, p):
        '''Calculates gamma, beta from their fourier representation u, v'''
        assert len(u) == len(v), 'length u and v should be equal'
        assert p >= 1, 'p must be a positive integer'
        
        q = len(u)
        k = np.arange(1,q+1)
        
        gamma = [None]*p
        beta = [None]*p
        
        for i in range(1,p+1):
            # note that the index i starts from 0 as opposed to 1
            gamma[i-1] = np.sum(u*np.sin((k-1/2)*(i-1/2)*np.pi/p))
            beta[i-1] =  np.sum(v*np.cos((k-1/2)*(i-1/2)*np.pi/p))
            
        return gamma, beta
    
    def find_local_amplitudes(self, u, v, p, optimizer = 'Nelder-Mead', optimizer_options = None):
        '''Find local optimum beginning from u, v'''
        assert len(u) == len(v), 'Lengths of amplitude arrays must be the same'
        
        def fun(amplitudes):
            ''' The objective function to be optimised by varying the angles
            Note, we want to maximize the expectation <Hc>, this is equivalent to 
            minimizing - <Hc>'''
            new_u, new_v  = amplitudes[:len(amplitudes)//2], amplitudes[len(amplitudes)//2:]
            new_gamma, new_beta = FOURIER.translate_fourier_to_angles(new_u, new_v, p)
            
            # maximize f = minimize -f 
            return -self.expectation(new_gamma, new_beta) 
        
        x0 = np.concatenate((u,v))
        result = scipy.optimize.minimize(fun, x0, method= optimizer)
        
        # finding angles
        amplitudes = result.x
        new_u = amplitudes[:len(amplitudes)//2]
        new_v = amplitudes[len(amplitudes)//2:]
        return list(new_u), list(new_v)
    
    def random_perturbation(amps, alpha=0.6):
        '''Returns a random perturbation sampled from a normal distribution (as described in Zhou, appendix B)
        with mean 0 and variance being the square of the corresponding amplitude
        included is a free parameter alpha, adjusting the strength of the perturbation
        empirically Zhou et al. found alpha = 0.6 to work well'''
        return [alpha*np.random.normal(0,a**2) for a in amps] 
    
    