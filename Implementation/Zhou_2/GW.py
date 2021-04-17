# -*- coding: utf-8 -*-
"""
Created on Tue Jun  9 14:12:40 2020

@author: joost
"""
from cvxgraphalgs.algorithms.max_cut import goemans_williamson_weighted 
import numpy as np

def find_cut(G):
    '''Returns cut using the Goemans-Williamson algorithm'''
    cut =  goemans_williamson_weighted(G)
    return cut

def find_bitstring(G):
    cut = find_cut(G)    
    return cut_to_bitstring(cut)
    
def cut_to_bitstring(cut):
    '''Translates a Cut object (from cvxgraphalgs) into a bitstring numpy array.
    The order is consistent with the QAOA.objective(G,x) convention for x
    
    For example, if cut.left = {0, 1, 3, 4} and cut.right = {2, 5}
    then the method returns [1,1,0,1,1,0].
    '''
    
    left = cut.left
    right = cut.right
    n = len(left)+len(right)
    
    bitstring = str(sum([10**i for i in left])) # nodes in left are 1, nodes in right are 0
    return np.array(list(map(int,list("0"*(n-len(bitstring)) + bitstring)))[::-1]) # it's ugly but it works
                
def evaluate_cut(G,cut):
    return cut.evaluate_cut_size(G)

