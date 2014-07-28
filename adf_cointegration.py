'''
Created July 27, 2014 

@author: Steven Sommer
@summary: Python script to download specified pairs price data from Yahoo Finance to a PANDAS DataFrame, plot the price
data, construct a scatter plot of pair prices, perform the ADF cointegration test results and print out the ADF 
Conintegration Test results.
'''

import datetime as dt
import pandas as pd
import pandas.io.data
from numpy import *
from matplotlib.pyplot import *
import statsmodels.api as sm
import statsmodels.tsa.stattools as ts
import matplotlib as mpl
import sys

# Specify Matplotlib figure size
mpl.rc('figure', figsize=(8, 7))

# Print Python, Pandas and Matplotlib versions
print 'Python ' + sys.version
print 'PANDAS ' + pd.__version__
print 'Matplotlib ' + mpl.__version__ + '\n'

# Construct the ADF Cointegration Test function
def cointegration_test(y, x):
    ols_result = sm.OLS(y, x).fit()
    return ts.adfuller(ols_result.resid)

#########################################################################
########################   MAIN CODE   ##################################
#########################################################################

if __name__ == "__main__":

    # Download historical price data from Yahoo Finance to a PANDAS DataFrame
    symbols = ['EWC','EWA']
    df = pd.io.data.get_data_yahoo(symbols, 
                               start=dt.datetime(2006, 4, 26), 
                               end=dt.datetime(2012, 4, 9))['Adj Close']

    # Print out the headers for the DataFrame
    print 'df headers' + '\n'
    print df.head()
    
    # Plot EWA and EWC prices
    #df.plot()
    #savefig('EWA_EWC_Cointegration_priceplot.pdf', format='pdf')
    
    # Construct the Scatter plot of EWC and EWA
    y = df['EWC']
    x = df['EWA']
    k = polyfit(x,y,1)
    xx = linspace(min(x),max(x),1000)
    yy = polyval(k,xx)

    # Plot the Scatter Plot of EWC and EWA
    plot(x,y,'o')
    plot(xx,yy,'r')
    savefig('EWA_EWC_Cointegration_plot.pdf', format='pdf')

    # Call the ADF Cointegration Test Function
    adf_coint = cointegration_test(y,x)
    
    # Print the ADF Cointegration Test Results
    print '\n' + 'ADF Cointegration Test' + '\n' + '\n' , adf_coint
    print '\n' + 'ADF:', adf_coint[0]
    print '\n' + 'p value:', adf_coint[1]
    print '\n' + 'Lag:', adf_coint[2]
    print '\n' + 'Observations used:', adf_coint[3]
    print '\n' + 'Critical Values:', adf_coint[4]
