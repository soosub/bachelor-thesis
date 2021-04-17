# -*- coding: utf-8 -*-
"""
Created on Sun Apr 26 20:27:33 2020

@author: joost
"""

from my_graphs import adjacency_matrix
import networkx as nx
import matplotlib.pyplot as plt

def brute_force(G, print_steps = False, plot=False):
    w = adjacency_matrix(G) 
    n = w.shape[0] #assuming, it's square
    
    best_cost_brute = 0
    xbest_brute = None
    for b in range(2**n):
        x = [int(t) for t in reversed(list(bin(b)[2:].zfill(n)))]
        cost = 0
        for i in range(n):
            for j in range(n):
                cost = cost + w[i,j]*x[i]*(1-x[j])
        if best_cost_brute < cost:
            best_cost_brute = cost
            xbest_brute = x 
        if print_steps:
            print('case = ' + str(x)+ ' cost = ' + str(cost))
    
    if plot:
        plt.figure()
        plt.title("Brute force approach")
        colors = ['r' if xbest_brute[i] == 0 else 'b' for i in range(n)]
        pos = nx.spring_layout(G)
        nx.draw_networkx(G, node_color=colors,node_size=600, alpha=.8, pos=pos)
    
    if print_steps:
        print('\nBest solution (by Brute force) = ' + str(xbest_brute) +\
                     ' cost = ' + str(best_cost_brute)) 
    return best_cost_brute