# -*- coding: utf-8 -*-
"""
Testing out the cvxgraphalgs package, in particular the Goemans-Williamson implementation
"""
from my_graphs import *
from cvxgraphalgs.algorithms.max_cut import goemans_williamson_weighted as gw

G = butterfly()

cut = gw(G)

print(cut.left, cut.right)
print(cut.evaluate_cut_size(G))