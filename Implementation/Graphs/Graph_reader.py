import networkx as nx
import matplotlib.pyplot as plt


def read_graph(filename):
    G = nx.readwrite.edgelist.read_weighted_edgelist(filename)
    return G

for i in range(2,5):
    G = read_graph('regular-3_10-nodes_graph'+str(i)+'.txt')
    plt.figure()
    nx.draw(G)