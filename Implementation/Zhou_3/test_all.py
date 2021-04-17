# -*- coding: utf-8 -*-
"""
Created on Tue Jun 23 13:54:54 2020

@author: joost
"""
# graphs
import networkx as nx

# solvers
from PSO import PSO
from GW import goemans_williamson
from INTERP import INTERP
from FOURIER import FOURIER

G =  nx.random_regular_graph(3,10)
p = 4

# Goemans Williamson
cut_value_GW = goemans_williamson(G)
print("GW", cut_value_GW)

# Particle swarm
pso = PSO(G)
gamma_pso, beta_pso = pso.get_angles_PSO(p, debug = True, maxiter = 10)
cut_value_pso = pso.best_sampled(gamma_pso,beta_pso)
print("PSO", cut_value_pso)

# INTERP
interp = INTERP(G)
gamma_int, beta_int = interp.get_angles_INTERP(p)
cut_value_interp = interp.best_sampled(gamma_int,beta_int)
print("INT", cut_value_interp)

# FOURIER
fourier = FOURIER(G)
gamma_four,beta_four = fourier.get_angles_FOURIER_constant(p, p)
cut_value_fourier = fourier.best_sampled(gamma_four,beta_four)
print("FOURIER", cut_value_fourier)

# Final result
print("------------------\n\n\nFinal results")
print("PSO", cut_value_pso)
print("GW", cut_value_GW)
print("INT", cut_value_interp)
print("FOURIER", cut_value_fourier)


