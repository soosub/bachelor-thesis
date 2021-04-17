# -*- coding: utf-8 -*-
"""
Created on Tue Apr 28 13:38:44 2020

@author: joost
"""
import matplotlib.pyplot as plt
import collections
import pandas as pd

def counter_histogram(results_counter, title="",):
    '''Creates a histogram from a Counter dictionary of results'''
    plt.figure()
    
    w = collections.Counter(results_counter)
    N = sum(w.values())
    
    d = {}
    for k, v in w.items():
        d[''.join(map(str,k))] = v/N

    df = pd.DataFrame(d.items(), columns=['state', 'count'])
    df = df.sort_values('state')
    plt.bar(df['state'], df['count'])
    
    plt.xlabel("state")
    plt.ylabel("probability within sample")
    plt.title(title)
    plt.show()
    