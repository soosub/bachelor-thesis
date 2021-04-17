# -*- coding: utf-8 -*-
"""
Created on Mon Jun  1 12:20:28 2020

@author: joost
"""

from QAOA_FOURIER import FOURIER
import qiskit
from my_graphs import diamond

G = diamond()
backend = qiskit.Aer.get_backend('qasm_simulator')
p = 5
q = 20

g,b = FOURIER.get_angles_FOURIER_constant(G,p,q,backend)

FOURIER.sample(G, g, b, backend, plot_histogram=True)