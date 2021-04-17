# -*- coding: utf-8 -*-
"""
Created on Mon Jun 29 14:12:54 2020

@author: joost
"""
import pandas as pd
import numpy as np
import ast

def string_to_numpyArray(x):
    return np.fromstring(x[1:-1],dtype = float, sep = ' ')

def load_csv(filename, GW = False):
    '''Loads a csv file with QAOA optimization data properly
    Warning: the structure of the file is very particular'''
    
    conv = {
    "betas":string_to_numpyArray,
    "counter":ast.literal_eval,
    "gammas":string_to_numpyArray,
    "graph":ast.literal_eval,
    "graph_type":ast.literal_eval,
    "most_common_bistring":ast.literal_eval,
    "n_Fp_evals":ast.literal_eval,
    "n_samples":ast.literal_eval,
    "p":ast.literal_eval,
    "qubit_order":ast.literal_eval,
    "seed":ast.literal_eval,
    "time":ast.literal_eval,
    }
    
    if GW:
        conv.update({'GW_samples':ast.literal_eval,
        'GW_mean':ast.literal_eval,
        'GW_std':ast.literal_eval,
        'GW_max':ast.literal_eval,
        'GW_min':ast.literal_eval,
        'Cmax':ast.literal_eval,
        'brute_time':ast.literal_eval,
        })

    return pd.read_csv(filename, converters = conv)