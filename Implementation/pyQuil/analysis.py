# -*- coding: utf-8 -*-
"""
Created on Wed May  6 13:08:14 2020

@author: joost
"""
import pandas as pd 


def analyse_file(fileName):
    # Read data from file 'filename.csv'  
    data = pd.read_csv("data/"+fileName+".csv") 
    
    # Preview the first 5 lines of the loaded data 
    return data
    
data = analyse_file("pyquil-diamond-qvm-p1")
