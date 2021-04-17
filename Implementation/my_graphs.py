# -*- coding: utf-8 -*-
"""
Created on Wed Apr  8 12:02:19 2020

@author: joost
"""
#import toools for math, graphs and plotting
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

def butterfly():
    '''Generating the butterfly graph with 5 nodes'''
    n     = 5
    V     = np.arange(0,n,1)
    E     =[(0,1,1.0),(0,2,1.0),(1,2,1.0),(3,2,1.0),(3,4,1.0),(4,2,1.0)] 
    
    G     = nx.Graph()
    G.add_nodes_from(V)
    G.add_weighted_edges_from(E)
    return G

def plot_graph(G): 
    # If G is an (adjacency) matrix, first make a graph object
    if type(G) == np.ndarray:
        G=nx.from_numpy_matrix(G)
        
    # Generate plot of the Graph
    colors       = ['r' for node in G.nodes()]
    default_axes = plt.axes(frameon=True)
    pos          = nx.spring_layout(G)
    
    nx.draw_networkx(G, node_color=colors, node_size=600, alpha=1, ax=default_axes, pos=pos)
    plt.show()
    
def diamond():
    '''
    Creates a diamond graph, i.e. a graph with 4 nodes and 5 edges 
    Also see https://www.graphclasses.org/smallgraphs.html#nodes4
    '''
    n = 4 # Number of nodes in graph
    G = nx.Graph()
    G.add_nodes_from(np.arange(0,n,1))
    elist = [(0,1,1.0),(0,2,1.0),(0,3,1.0),(1,2,1.0),(2,3,1.0)]
    
    # tuple is (i,j,weight) where (i,j) is the edge
    G.add_weighted_edges_from(elist)
    
    return G

def adjacency_matrix(G):
    '''Computes the weight matrix of a graph (aka adjacency matrix) from a graph object'''
    return np.array(nx.to_numpy_matrix(G))

def cycle_graph(n, w=1):
    '''Creates cyclic graph of n nodes'''
    G= nx.empty_graph(n)
    for v in range(n-1):
        G.add_edge(v,v+1, weight = w)
    if n>1: G.add_edge(n-1,0,weight = w)
    return G # maybe make a class that inherits from networkx instead of defining such functions?
  
def random_regular(d,n):
    return nx.random_regular_graph(d, n)

def random_regular_weighted(d,n):
    '''Generates a random regular weighted graph,
    with edge weights drawn from a uniform distribution from 0 to 1'''
    G = nx.random_regular_graph(d, n)
    for (u, v) in G.edges():
        G.edges[u,v]['weight'] = np.random.uniform()
    return G

def randomize_weights(G, low=0, up = 1):
    '''Reassigns weights determined by sampling from a uniform distribution [low, up]'''
    Gcopy = G.copy()
    for (u, v) in Gcopy.edges():
        Gcopy.edges[u,v]['weight'] = np.random.uniform(low,up)
    return Gcopy
    