# -*- coding: utf-8 -*-
"""
Created on Fri Jun  5 12:57:50 2020

@author: joost
"""
#import test_interp
import cProfile

from QAOA_INTERP import INTERP
import qiskit
from my_graphs import diamond


G = diamond() # 4 nodes
backend = qiskit.Aer.get_backend('qasm_simulator')
p = 4

cProfile.run("INTERP.get_angles_INTERP(G, p, backend)", 'QAOA-profile-p4')
