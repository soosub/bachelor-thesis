# -*- coding: utf-8 -*-
"""
Created on Wed May  6 12:32:09 2020

@author: joost

analysis of data
"""

import pandas as pd 
import glob

fileNames = glob.glob("data/*.csv")
fileName = fileNames[24]
print(fileName)

data = pd.read_csv(fileName)
for x in list(data.columns.values):
    print(x)
    
print()    
# Preview the first 5 lines of the loaded data
print(data['graph'][0]+', p =', data['p'][0])

# Time and iterations
print("iterations average (s) ", data['iterations'].mean())
print("iterations std (s) ", data['iterations'].std())

print("time average (s) ", data['time'].mean())
print("time std (s) ", data['time'].std())

# Solution objective
print("solution objective (mean)", data['solution objective'].mean())
print("solution objective (max)", data['solution objective'].max())
print("solution objective (min)", data['solution objective'].min())

# Fp
print("energy (mean)", data['energy'].mean())
print("energy (std)", data['energy'].std())