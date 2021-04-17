# -*- coding: utf-8 -*-
"""
Created on Thu Jul  2 22:22:51 2020

@author: joost
"""
import pandas as pd
from data_load import load_csv
import numpy as np
from pyquil_base import brute_force
from tqdm import tqdm
import networkx as nx
from GW import goemans_williamson as gw

# Comparing runtime of RI and INT

# unweighted
dfu1 = load_csv('data/data_3-regular_unweighted_INT_12.csv')
dfu2 = load_csv('data/data_3-regular_unweighted_INT_14.csv')
dfu3 = load_csv('data/data_3-regular_unweighted_INT_8-10-16.csv')

# weighted
dfw1 = load_csv('data/data_3-regular_weighted_INT_8-10-12.csv')
dfw2 = load_csv('data/data_3-regular_weighted_INT_14-16.csv')

# loading the data s.t. they are equivalent (same p, same N)
p_max = 8
seed_max = 20
# unweighted
u8 = dfu3.loc[lambda df: df['p'] <= p_max, :].loc[lambda df: df['seed'] < seed_max, :].loc[lambda df: df['n_nodes'] == 8, :]
u10 = dfu3.loc[lambda df: df['p'] <= p_max, :].loc[lambda df: df['seed'] < seed_max, :].loc[lambda df: df['n_nodes'] == 10, :]
u12 = dfu1.loc[lambda df: df['p'] <= p_max, :].loc[lambda df: df['seed'] < seed_max, :].loc[lambda df: df['n_nodes'] == 12, :]
u14 = dfu2.loc[lambda df: df['p'] <= p_max, :].loc[lambda df: df['seed'] < seed_max, :].loc[lambda df: df['n_nodes'] == 14, :]
u16 = dfu3.loc[lambda df: df['p'] <= p_max, :].loc[lambda df: df['seed'] < seed_max, :].loc[lambda df: df['n_nodes'] == 16, :] # this one is truncated (reading csv while it was written to)

# weighted
w8 = dfw1.loc[lambda df: df['p'] <= p_max, :].loc[lambda df: df['seed'] < seed_max, :].loc[lambda df: df['n_nodes'] == 8, :]
w10 = dfw1.loc[lambda df: df['p'] <= p_max, :].loc[lambda df: df['seed'] < seed_max, :].loc[lambda df: df['n_nodes'] == 10, :]
w12 = dfw1.loc[lambda df: df['p'] <= p_max, :].loc[lambda df: df['seed'] < seed_max, :].loc[lambda df: df['n_nodes'] == 12, :]
w14 = dfw2.loc[lambda df: df['p'] <= p_max, :].loc[lambda df: df['seed'] < seed_max, :].loc[lambda df: df['n_nodes'] == 14, :]
w16 = dfw2.loc[lambda df: df['p'] <= p_max, :].loc[lambda df: df['seed'] < seed_max, :].loc[lambda df: df['n_nodes'] == 16, :]

dfs_u = [u8,u10,u12,u14,u16]
dfs_w = [w8,w10,w12,w14,w16]
if np.std([len(df) for df in dfs_u+dfs_w]) != 0:
    raise Warning("Inconsistency in data")

# calculating missing data
for df in [u12,u14,w14,w16]:
    Cmax = []
    GW_samples = []
    GW_mean = []
    GW_std = []
    GW_max = []
    GW_min = []
    GW_bound = []
    for i in tqdm(range(0,len(df),p_max)):
        G = nx.from_dict_of_dicts(df.iloc()[i]['graph'])
        
        # brute force
        if 'Cmax' not in df:
            Cmax_i = brute_force(G)
            Cmax = Cmax + p_max*[Cmax_i]
        
        # Goemans-Williamson
        if 'GW_samples' not in df:
            gw_samples = [gw(G) for _ in range(10)]
            gw_mean = np.mean(gw_samples)
            gw_std = np.std(gw_samples)
            gw_max = np.max(gw_samples)
            gw_min = np.min(gw_samples)
            gw_bound = 0.878 * Cmax_i
            
            GW_samples += [gw_samples]*p_max
            GW_mean += [gw_mean]*p_max
            GW_std += [gw_std]*p_max
            GW_max += [gw_max]*p_max
            GW_min += [gw_min]*p_max
            GW_bound += [gw_bound]*p_max
        
    if 'Cmax' not in df:
        df.insert(2, "Cmax", Cmax) 
    if 'GW_samples' not in df:
        df.insert(2, "GW_samples", GW_samples) 
        df.insert(2, "GW_mean", GW_mean) 
        df.insert(2, "GW_std", GW_std) 
        df.insert(2, "GW_max", GW_max) 
        df.insert(2, "GW_min", GW_min) 
        df.insert(2, "GW_bound", GW_bound) 
    
    
u8.loc[:, ~u8.columns.str.contains('^Unnamed')].to_csv('data_trim/data_trim_3-regular_unweighted_INT_8.csv')
u10.loc[:, ~u10.columns.str.contains('^Unnamed')].to_csv('data_trim/data_trim_3-regular_unweighted_INT_10.csv')
u12.loc[:, ~u12.columns.str.contains('^Unnamed')].to_csv('data_trim/data_trim_3-regular_unweighted_INT_12.csv')
u14.loc[:, ~u14.columns.str.contains('^Unnamed')].to_csv('data_trim/data_trim_3-regular_unweighted_INT_14.csv')
u16.loc[:, ~u16.columns.str.contains('^Unnamed')].to_csv('data_trim/data_trim_3-regular_unweighted_INT_16.csv')

w8.loc[:, ~w8.columns.str.contains('^Unnamed')].to_csv('data_trim/data_trim_3-regular_weighted_INT_8.csv')
w10.loc[:, ~w10.columns.str.contains('^Unnamed')].to_csv('data_trim/data_trim_3-regular_weighted_INT_10.csv')
w12.loc[:, ~w12.columns.str.contains('^Unnamed')].to_csv('data_trim/data_trim_3-regular_weighted_INT_12.csv')
w14.loc[:, ~w14.columns.str.contains('^Unnamed')].to_csv('data_trim/data_trim_3-regular_weighted_INT_14.csv')
w16.loc[:, ~w16.columns.str.contains('^Unnamed')].to_csv('data_trim/data_trim_3-regular_weighted_INT_16.csv')


