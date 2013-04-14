'''
Created on April 12, 2013

@author Steven Sommer
@Summary: Portfolio Sortino Ratio Optimizer by adjusting allocations. This is a variant of the HW1 script which uses the optimal Sortino Ratio to determine the the optimal portfolio allocations. The appeal of using the Sortino Ratio is that it only penalizes the daily portfolio performance for the negative moment (negative volatility). Created script as an experiment to see if there are any differences in allocations and cumulative return based on optimization by optimal Sortino Ration vs Sharpe Ratio.
Note: This version runs very, very fast!
'''
# QSTK Imports
import QSTK.qstkutil.qsdateutil as du
import QSTK.qstkutil.tsutil as tsu
import QSTK.qstkutil.DataAccess as da

# Third Party Imports
import datetime as dt
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import math

print "Pandas Version", pd.__version__

#
# Create Analyse Function
#
def analyse(na_close, ls_allocations):

    # Normalize the close price
    na_norm_close = na_close / na_close[0,:]

    # Get weighted daily returns
    weighted_daily_close = np.dot(na_norm_close,ls_allocations)

    # Copy the weighted daily close to a new ndarray to find returns
    port_daily_ret = weighted_daily_close.copy()

    # Calculate daily returns of the portfolio close price
    tsu.returnize0(port_daily_ret)

    # Get average portfolio daily returns
    daily_ret = np.average(port_daily_ret)

    # Calculate negative daily returns and Sortino Ratio
    negative_port_daily_ret = port_daily_ret[port_daily_ret < 0]
    sortino_dev = np.std( negative_port_daily_ret, axis=0 )
    sortino = (daily_ret / sortino_dev) * np.sqrt(252)

    # Calculate volatility of average weighted daily returns
    vol = np.std(port_daily_ret)

    # Calculate Sharpe Ratio
    k = math.sqrt(252)
    sharpe = k * (daily_ret/vol)

    # Calculate Cumulative Return
    cum_ret = np.dot((na_close[-1]/na_close[0]),ls_allocations)

    return vol, daily_ret, sortino, sharpe, cum_ret

#
# Create Optimize function
#

def optimize(na_close, verbose=False):

    # Generate all possible combinations of allocations
    # Filter for permitted combinations of allocations
    # Call simulate function, calculate Sharpe Ratio and select best Sharpe Ratio

    optimal_sortino = -100
    optimal_allocation = [0.0 ,0.0 ,0.0 ,0.0]
    optimal_vol = 0
    optimal_daily_ret = 0
    optimal_cum_ret = 0

    count = 0
    count2 = 0
    for w in np.arange(0,1.1,0.1):
        for x in np.arange(0,1.1,0.1):
            for y in np.arange(0,1.1,0.1):
                for z in np.arange(0,1.1,0.1):
                    count = count + 1
                    ls_allocations = [w, x, y, z]
                    ls_allocations = np.transpose(ls_allocations)
                    alloc_total =  w + x + y + z
                    if alloc_total == 1:
                        count2 = count2 + 1
                        # Call analyse function
                        vol, daily_ret, sortino, sharpe, cum_ret = analyse(na_close, ls_allocations)
                        if sortino > optimal_sortino:
                            optimal_sortino = sortino
                            optimal_allocation = ls_allocations
                            optimal_vol = vol
                            optimal_daily_ret = daily_ret
                            optimal_cum_ret = cum_ret
    if verbose:
        print "Possible Allocations:",count
        print "Permitted Allocations:",count2
    return optimal_sortino, optimal_allocation, optimal_vol, optimal_daily_ret, optimal_cum_ret
    
######################################
############ MAIN CODE ###############
######################################

# List of symbols
ls_symbols = ['BRCM', 'TXN', 'AMD', 'ADI']

# List of allocations
ls_allocations = [0.4, 0.0, 0.2, 0.4]

# Start and End date of the charts
dt_start = dt.datetime(2010, 1, 1)
dt_end = dt.datetime(2010, 12, 31)

# Keys to read from data
ls_keys = ['open', 'high', 'low', 'close', 'volume', 'actual_close']

# We need closing prices so the timestamp should be hours=16
dt_timeofday = dt.timedelta(hours=16)

# Get a list of trading days between the start and the end
#if verbose:
print "Get NYSE trading days"
dt_timestamps = du.getNYSEdays(dt_start, dt_end, dt_timeofday)
#print "NYSE trading day for",dt_start.strftime("%Y"),":", len(dt_timestamps)

# Creating an object of the dataaccess class with Yahoo as the source
c_dataobj = da.DataAccess('Yahoo', cachestalltime=0)

# Reading the data, now d_data is a dictionary with the keys above.
# Timestamps and symbols are the ones that were specified before.
#if verbose:
print "Start reading data"
ldf_data = c_dataobj.get_data(dt_timestamps, ls_symbols, ls_keys)
d_data = dict(zip(ls_keys, ldf_data))
#if verbose:
print "Finished reading data"

# Getting numpy nda array of close prices
na_close = d_data['close'].values

# Call simulate function
#vol, daily_ret, sharpe, cum_ret = simulate(dt_start, dt_end, ls_symbols, ls_allocations, verbose=True)

# Call optimize function
optimal_sortino, optimal_allocation, optimal_vol, optimal_daily_ret, optimal_cum_ret = optimize(na_close, verbose=True)

#
# Required Output
#
print "Start Date: ", dt_start.strftime("%B %d, %Y")
print "End Date: ", dt_end.strftime("%B %d, %Y")
print "Symbols: ", ls_symbols
print "Optimal Allocations: ", optimal_allocation
print "Sortino Ratio: ", optimal_sortino
print "Volatility (stdev of daily returns): ", optimal_vol
print "Average Daily Return: ", optimal_daily_ret
print "Cumulative Return: ", optimal_cum_ret
