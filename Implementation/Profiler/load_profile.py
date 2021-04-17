# -*- coding: utf-8 -*-
"""
Created on Mon Jun 15 14:34:17 2020

@author: joost
"""

import pstats
import io

filename = 'pso-self'

category = 'tottime' #tottime, ncalls, cumtime

s = io.StringIO()
ps = pstats.Stats(filename, stream=s).sort_stats(category) 
ps.print_stats()

with open('profile_'+filename+'_'+category+'.txt', 'w+') as f:
    f.write(s.getvalue())