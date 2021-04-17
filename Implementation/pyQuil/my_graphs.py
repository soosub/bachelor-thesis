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

def plot_graph(G, labels, edge_weight=False):
    '''Draws graph'''
    # names of the nodes if not set already
    print("Labels:", labels)
        
    # If G is an (adjacency) matrix, first make a graph object
    if type(G) == np.ndarray:
        G=nx.from_numpy_matrix(G)
        
    # Generate plot of the Graph    
    colors       = ['r' for node in G.nodes()]
    default_axes = plt.axes(frameon=True)
    pos = nx.spring_layout(G)
    nx.draw(G, node_color=colors, node_size=600, alpha=1, ax=default_axes, pos=pos)
    
    # label nodes and edges
    print("labels")
    nx.draw_networkx_labels(G, pos, {key: value for (key, value) in enumerate(labels)}) #keyError :(                         
    if edge_weight:
        edge_labels = nx.get_edge_attributes(G,'weight')
        nx.draw_networkx_edge_labels(G,pos,edge_labels=edge_labels)    
        
    plt.show()
    
def plot_cut(G, bitstring):
    '''Draws graph and colour codes the cut'''
    print("plot_cut is yet to be implemented")
    
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
    '''Compute the weight matrix of a graph (a.k.a. adjacency matrix) from a networkx graph object '''
    n = len(G)
    w = np.zeros([n,n])
    for i in range(n):
        for j in range(n):
            temp = G.get_edge_data(i,j,default=0)
            if temp != 0:
                w[i,j] = temp['weight']
    return w

def cycle_graph(n, w=1):
    '''Creates cyclic graph of n nodes'''
    G= nx.empty_graph(n)
    for v in range(n-1):
        G.add_edge(v,v+1, weight = w)
    if n>1: G.add_edge(n-1,0,weight = w)
    return G # maybe make a class that inherits from networkx instead of defining such functions?
    
def random_regular(d,n):
    return nx.random_regular_graph(d, n)
    
