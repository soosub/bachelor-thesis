# -*- coding: utf-8 -*-
"""
Created on Sat Jun 27 23:24:05 2020

@author: joost
"""

import networkx as nx

N_graphs = 10

n = 10
d = 3
graph_type = 'regular'


for i in range(N_graphs):
    G = nx.random_regular_graph(d,n, seed = i)
    
    for (u, v) in G.edges():
            if G.edges[u,v] == {}:
                G.edges[u,v]['weight'] = 1
                
    filename = graph_type+'-'+str(d)+'_'+str(n)+'-nodes_graph'+str(i)+'.txt'
    print(filename)
    nx.write_weighted_edgelist(G,filename)