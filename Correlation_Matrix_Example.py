'''
Created April 6, 2014

@author: Steven Sommer
@summary: Python script to download historical price data from Yahoo Finance to
a PANDAS DataFrame, construct and print a Correlation Matrix, constuct a
Correlation Heat Map and save that plot as a PDF file.
'''

# Imports
import datetime as dt
import pandas as pd
import pandas.io.data
from pandas import Series, DataFrame
import matplotlib.pyplot as plt
import matplotlib as mpl
import sys

# Specify Matplotlib figure size
mpl.rc('figure', figsize=(8, 7))

# Print Python, Pandas and Matplotlib versions
print 'Python ' + sys.version
print 'PANDAS ' + pd.__version__
print 'Matplotlib ' + mpl.__version__ + '\n'

# Download historical price data from Yahoo Finance to a PANDAS DataFrame
df = pd.io.data.get_data_yahoo(['AAPL', 'GE', 'HPQ', 'IBM', 'KO', 'MSFT', 'PEP'], 
                               start=dt.datetime(2010, 1, 1), 
                               end=dt.datetime(2013, 1, 1))['Adj Close']

# Print out the headers for the DataFrame
print 'DataFrame headers' + '\n'
print df.head()

# Calculate daily returns for the Tickers in the DataFrame
rets = df.pct_change()

# Calculate the Correlation for the daily returns of the Tickers
corr = rets.corr()

# Print the Correlation Matrix
print '\n' + 'Correlation Matrix' + '\n'
print corr

# Create a Correlatin Matrix Heat Map and save to a PDF file
print '\n' + 'Creating a Correlation Matrix Heat Map and saving to PDF file'
plt.imshow(corr, cmap='hot', interpolation='none')
plt.colorbar()
plt.xticks(range(len(corr)), corr.columns)
plt.yticks(range(len(corr)), corr.columns);

plt.savefig('Correlation_Matrix_Example.pdf', format='pdf')
