'''
Created on April 6, 2014

@author: Steven Sommer
@summary: Python script to download historical price data from Yahoo Finance to
a PANDAS DataFrame, construct a Markowitz Plot and save that plot as a PDF file.
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

# Create the annotated Markowitz Plot and save to a PDF file
print '\n' + 'Creating annotated Markowitz Plot and saving to PDF file'
plt.scatter(rets.std(), rets.mean())
plt.xlabel('Risk')
plt.ylabel('Expected returns')
for label, x, y in zip(rets.columns, rets.std(), rets.mean()):
    plt.annotate(
        label, 
        xy = (x, y), xytext = (20, -20),
        textcoords = 'offset points', ha = 'right', va = 'bottom',
        bbox = dict(boxstyle = 'round,pad=0.5', fc = 'yellow', alpha = 0.5),
        arrowprops = dict(arrowstyle = '->', connectionstyle = 'arc3,rad=0'))

plt.savefig('Markowitz_Plot_Example_1.pdf', format='pdf')
