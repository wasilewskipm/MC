"""
Created on Thu Jan 16 11:01:53 2020

@author: ADM-QPW
"""

import datetime as dt
import math as m
import random as rnd

# number of iterations
simnum = 1000

for ii in range(simnum):
    
    # start date of MC simulation
    simstart = dt.datetime(2020, 1, 1, 0, 0, 0)
    # end date of MC simulation
    simend = dt.datetime(2030, 12, 31, 23, 59, 59)
    
    # last failure date
    lfdt = dt.datetime(2018, 10, 31, 0, 0, 0)
    
    # wb parameters
    beta, eta = 2.0, 1000

    # loop until last failure date is greater than simend
    while lfdt < simend:
        # accumulated time since last failure
        acctime = max([(simstart - lfdt).days, 0])
        
        # minimal unreliability based on acctime
        minunrel = 1 - m.exp(-(acctime/eta)**beta)
        
        # generate random number from minunrel to 1.0
        rndunrel = rnd.uniform(minunrel, 1)
        
        # calculate failure date based on rndunrel
        rnddt = -eta * m.log((1-rndunrel)**1/beta)
        
        # calcuate new failure date
        lfdt += dt.timedelta(days = rnddt)
        
        # print the result of loop
        print('iteration ' + str(ii) + ', failure on ' + str(lfdt))