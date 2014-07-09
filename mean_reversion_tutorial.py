'''
Created March 19, 2014

@author: Steven Sommer (from Michael Halls-Moore's Mean Reversion Tutorial)
@summary: Python script to look for Mean Reversion in time series data by application
of the Augmented Dickey-Fuller (ADF) Test and, alternatively, testing for stationarity
by the calculation of the Hurst Exponent. Please note that you must have patsy and statsmodels 
installed to run this script. Note: Google symbol edited on May 7, 2014 to reflect the recent 
changes to the Google symbols due to the split of the shares in Class A and Class C stock: 
GOOG = Class C stock and GOOGL = Class A stock. 
'''

# Import the Time Series library
import statsmodels.tsa.stattools as ts

# Import Datetime and the Pandas DataReader
from datetime import datetime
from pandas.io.data import DataReader

# Import from Numpy
from numpy import cumsum, log, polyfit, sqrt, std, subtract
from numpy.random import randn

# Download the Google OHLCV data from 1/1/2000 to 1/1/2013
googl = DataReader("GOOGL", "yahoo", datetime(2000,1,1), datetime(2013,1,1))

# Output the results of the Augmented Dickey-Fuller test for Google
# with a lag order value of 1
Augdf = ts.adfuller(googl['Adj Close'], 1)
print Augdf

# Hurst Exponent Calculation

def hurst(ts):
    """Returns the Hurst Exponent of the time series vector ts"""
    # Create the range of lag values
    lags = range(2, 100)

    # Calculate the array of the variances of the lagged differences
    tau = [sqrt(std(subtract(ts[lag:], ts[:-lag]))) for lag in lags]

    # Use a linear fit to estimate the Hurst Exponent
    poly = polyfit(log(lags), log(tau), 1)

    # Return the Hurst exponent from the polyfit output
    return poly[0]*2.0

# Create a Gometric Brownian Motion, Mean-Reverting and Trending Series
gbm = log(cumsum(randn(100000))+1000)
mr = log(randn(100000)+1000)
tr = log(cumsum(randn(100000)+1)+1000)

# Output the Hurst Exponent for each of the above series
# and the price of Google (the Adjusted Close price) for 
# the ADF test given above in the article
print "Hurst(GBM):   %s" % hurst(gbm)
print "Hurst(MR):    %s" % hurst(mr)
print "Hurst(TR):    %s" % hurst(tr)

# Assuming you have run the above code to obtain 'googl'!
print "Hurst(GOOGL):  %s" % hurst(googl['Adj Close'])
