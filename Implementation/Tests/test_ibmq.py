# -*- coding: utf-8 -*-
"""
Created on Thu Jun  4 13:38:00 2020

@author: joost
"""

from qiskit import IBMQ
from QAOA import QAOA
import my_graphs

G = my_graphs.diamond()
p = 1
gamma, beta = [0], [0]

provider = IBMQ.load_account()
backend = provider.get_backend('ibmq_qasm_simulator')

QAOA.sample(G, gamma, beta, backend, n_samples = 1024, plot_histogram = False)