"""
Created on Thu Jan 16 11:01:53 2020

@author: ADM-QPW
"""

import datetime as dt
import random as rnd
import pandas as pd
import numpy as np

# number of iterations
simnum = 1000

# initialize df for results
simdf = pd.DataFrame(columns = ['iter', 'id', 'lastf'])

for ii in range(simnum):
    
    # start date of MC simulation
    simstart = dt.datetime(2020, 1, 1, 0, 0, 0)
    
    # end date of MC simulation
    simend = dt.datetime(2030, 12, 31, 23, 59, 59)
    
    # dummy dataframe
    eventdf = pd.DataFrame([[101, dt.datetime(2018, 10, 31, 0, 0, 0), 0.0], 
                            [102, dt.datetime(2018, 11, 11, 0, 0, 0), 0.0]],
                            columns = ['id', 'lastf', 'rndunrel'])

    # wb parameters
    beta, eta = 2.0, 1000

    # loop until last failure date is greater than simend
    while any(eventdf.lastf < simend):
        
        # nested below calc for dataframe 
        ## accumulated time since last failure
        ## acctime = (simstart - lfdt).days
        ## minimal unreliability based on acctime
        ## minunrel = 1 - m.exp(-(acctime/eta)**beta)
        ## generate random number from minunrel to 1.0
        ## rndunrel = rnd.uniform(minunrel, 1)
        if any(eventdf.lastf < simstart):
            eventdf.rndunrel = np.random.uniform(1 - np.exp(-((simstart - eventdf.lastf)/np.timedelta64(1, 'D')/eta)**beta), 1)
        else:
            eventdf.rndunrel = np.random.uniform(0, 1, eventdf.shape[0])
        
        # nested below calc for dataframe
        ## calculate days to failure based on rndunrel
        ## rnddtf = -eta * m.log((1-rndunrel)**1/beta)      
        ## calcuate new failure date
        ## lfdt += dt.timedelta(days = rnddtf)
        eventdf.lastf += (-eta * np.log((1-eventdf.rndunrel)**1/beta)).map(dt.timedelta)
        
        # append results to final df
        simdf = simdf.append(eventdf[eventdf.lastf < simend][['id', 'lastf']], ignore_index=True, sort=False)
        simdf.iter.fillna(value=ii, inplace=True)

# print results      
print(simdf)