'''
Created on March 14, 2013

@author: Steven Sommer
@summary: Script scans SP500 for desired events and creates a graphic summary of all events within the designated time series. This script is modified to scan for event in which the price has fallen below a given price. The commented out lines were left in the code to enable adaptation of the code for a percentage price change vs the SP500. This script borrows heavily from the QSTK - Event Profiler Tutorial.
'''

from pylab import *
import pandas as pd
import numpy as np
import math
import copy
import QSTK.qstkutil.qsdateutil as du
import datetime as dt
import QSTK.qstkutil.DataAccess as da
import QSTK.qstkutil.tsutil as tsu
import QSTK.qstkstudy.EventProfiler as ep

"""
Accepts a list of symbols along with start and end date
Returns the Event Matrix which is a pandas Datamatrix
Event matrix has the following structure :
    |IBM |GOOG|XOM |MSFT| GS | JP |
(d1)|nan |nan | 1  |nan |nan | 1  |
(d2)|nan | 1  |nan |nan |nan |nan |
(d3)| 1  |nan | 1  |nan | 1  |nan |
(d4)|nan |  1 |nan | 1  |nan |nan |
...................................
...................................
Also, d1 = start date
nan = no information about any event.
1 = status bit(positively confirms the event occurence)
"""


def find_events(ls_symbols, d_data):
    ''' Finding the event dataframe '''
    df_close = d_data['actual_close']
    ts_market = df_close['SPY']

    print "Finding Events"

    # Creating an empty dataframe
    df_events = copy.deepcopy(df_close)
    df_events = df_events * np.NAN

    # Time stamps for the event range
    ldt_timestamps = df_close.index

    for s_sym in ls_symbols:
        for i in range(1, len(ldt_timestamps)):
            # Calculating the returns for this timestamp
            f_symprice_today = df_close[s_sym].ix[ldt_timestamps[i]]
            f_symprice_yest = df_close[s_sym].ix[ldt_timestamps[i - 1]]
            #f_marketprice_today = ts_market.ix[ldt_timestamps[i]]
            #f_marketprice_yest = ts_market.ix[ldt_timestamps[i - 1]]
            #f_symreturn_today = (f_symprice_today / f_symprice_yest) - 1
            #f_marketreturn_today = (f_marketprice_today / f_marketprice_yest) - 1

            # Event is found if the symbol has been trading above $5 and drops below $5
            if f_symprice_yest >= 6.0 and f_symprice_today < 6.0:
                df_events[s_sym].ix[ldt_timestamps[i]] = 1
                #print s_sym, i, ldt_timestamps[i], f_symprice_yest, f_symprice_today
                
    return df_events


if __name__ == '__main__':
    
    dataobj = da.DataAccess('Yahoo', cachestalltime=0)
    ls_symbols = dataobj.get_symbols_from_list('sp5002012')
    ls_symbols.append('SPY')
    ls_all_symbols = dataobj.get_all_symbols()
    intersectsyms = list(set(ls_all_symbols) & set(ls_symbols)) # valid symbols
    badsyms = []
    if size(intersectsyms)<size(ls_symbols):
        badsyms = list(set(ls_symbols) - set(intersectsyms))
        print "warning: portfolio contains symbols that do not exist:" 
        print badsyms
    for i in badsyms: # remove the bad symbols from our portfolio
        index = ls_symbols.index(i)
        ls_symbols.pop(index)
        #portalloc.pop(index)

    # Read the historical data in from our data store
    dt_start = dt.datetime(2008, 1, 1)
    dt_end = dt.datetime(2009, 12, 31)
    ldt_timestamps = du.getNYSEdays(dt_start, dt_end, dt.timedelta(hours=16))
    ls_keys = ['open', 'high', 'low', 'close', 'volume', 'actual_close']
    ldf_data = dataobj.get_data(ldt_timestamps, ls_symbols, ls_keys)
    d_data = dict(zip(ls_keys, ldf_data))

    # Remove NAN from the price data
    for s_key in ls_keys:
        d_data[s_key] = d_data[s_key].fillna(method = 'ffill')
        d_data[s_key] = d_data[s_key].fillna(method = 'bfill')
        d_data[s_key] = d_data[s_key].fillna(1.0)

    df_events = find_events(ls_symbols, d_data)
    print "Creating Study"
    ep.eventprofiler(df_events, d_data, i_lookback=20, i_lookforward=20,
                s_filename='QuizQ3SP2012.pdf', b_market_neutral=True, b_errorbars=True,
                s_market_sym='SPY')
