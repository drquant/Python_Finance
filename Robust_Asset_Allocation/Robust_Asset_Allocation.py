''''
Created May 3, 2015

@author: Steven Sommer, MD, MBA
@summary: Python script to download historical price data from Yahoo Finance to a PANDAS DataFrame, construct a moderate 
Robust Allocation Portfolio (modified Ivy Portfolio concept developed by Wesley Gray of Alpha Architect), print a graph 
of the cumulative returns to a PDF file, and print out the weights of the current portfolio holdings.
Note: This script was developed in Python 2.7.6.
'''

# Imports
import datetime as dt
import pandas as pd
import pandas.io.data
from pandas import Series, DataFrame
import matplotlib.pyplot as plt
import matplotlib as mpl
import sys
import numpy as np
import math
import portfolio_metrics_monthly as pmm

# Specify Matplotlib figure size
mpl.rc('figure', figsize=(8, 7))

# Print Python, Pandas and Matplotlib versions
print 'Python ' + sys.version
print 'PANDAS ' + pd.__version__
print 'Numpy ' + np.__version__
print 'Matplotlib ' + mpl.__version__ + '\n'
    
# Define a list of ticker symbols
symbols = ['PRF','PDP','GVAL','PIZ','VNQ','DBC','BND','SHY']

# Download historical price data from Yahoo Finance to a PANDAS DataFrame
df = pd.io.data.get_data_yahoo(symbols, 
                               start=dt.datetime(2014, 3, 12), 
                               end=dt.datetime(2015, 12, 4))['Adj Close']

print df.head()

# Calculate the daily returns
rets = df.pct_change()

# Define the maximum allowed fully invested asset weights for each asset
# Weights used in this model correspond the the moderate Robust portfolio
wt = [0.15,0.15,0.15,0.15,0.10,0.10,0.20]
symbols1 = ['PRF','PDP','GVAL','PIZ','VNQ','DBC','BND']
max1 = pd.DataFrame(index=rets.index, columns=symbols1)

days = 0
for i in rets.index:
    c = 0
    for sym in symbols1:
        max1[sym][i] = wt[c]
        c = c + 1
    days = days + 1
'''
# Asset weight total check (maximum asset weights must sum to 1.0)
total_weight = 0
for sym in symbols:
    total_weight = total_weight + max1[sym]
if total_weight == 1:
    print 'Total maximal asset weight sum to 1.0!'
else:
    print 'ERROR: Maximum assigned maximum asset weights <> 1.0!'
'''
# Calculate 200 day SMA
sma200 = pd.rolling_mean(df, 200)

# Calculate the 200 day asset Beta (Rasset - Rf)
# Step 1 - Calculate the 200 day asset returns
asset_return = df.pct_change(200)

# Step 2 - Calculate the 200 day asset Betas
# Step 2a - Create a PANDAS DataFrame for the asset Betas
beta = pd.DataFrame(index=rets.index, columns=symbols)

# Step 2b - Populate the PANDAS DataFrame with the asset Betas
for i in rets.index:
    for sym in symbols:
        beta[sym][i] = asset_return[sym][i] - asset_return['SHY'][i]

# Calculate the dynamic asset weights
# Step 1 - Create a PANDAS DataFrame for the dynamic asset weights
asset_wt_ma = pd.DataFrame(index=rets.index, columns=symbols1)
asset_wt_beta = pd.DataFrame(index=rets.index, columns=symbols1)
asset_wt_tot = pd.DataFrame(index=rets.index, columns=symbols1)

for i in rets.index:
    for sym in symbols1:
        if df[sym][i] > sma200[sym][i]:
            asset_wt_ma[sym][i] = max1[sym][i]/2
        elif df[sym][i] <= sma200[sym][i]:
            asset_wt_ma[sym][i] = 0
        if beta[sym][i] > 0:
            asset_wt_beta[sym][i] = max1[sym][i]/2
        elif beta[sym][i] <= 0:
            asset_wt_beta[sym][i] = 0

for i in rets.index:
    for sym in symbols1:
        asset_wt_tot[sym][i] = asset_wt_ma[sym][i] + asset_wt_beta[sym][i]
            
exposure = asset_wt_tot.sum(axis=1)
shy_wt = 1 - exposure

rets['Robust'] = Series(np.nan, index=rets.index)

for i in rets.index:
    rets['Robust'][i] = (asset_wt_tot['PRF'][i] * rets['PRF'][i]) + (asset_wt_tot['PDP'][i] * rets['PDP'][i]) + (asset_wt_tot['GVAL'][i] * rets['GVAL'][i]) + (asset_wt_tot['PIZ'][i] * rets['PIZ'][i]) + \
    (asset_wt_tot['VNQ'][i] * rets['VNQ'][i]) + (asset_wt_tot['DBC'][i] * rets['DBC'][i]) +  (asset_wt_tot['BND'][i] * rets['BND'][i]) + (shy_wt[i] * rets['SHY'][i])

norm_rets = rets.cumsum()
norm_rets.plot()
plt.savefig('Robust_Asset_Allocation_-_2014_-_2015.pdf', format='pdf')

print '\n' + 'Current Robust Portfolio Asset Allocations:' + '\n'

for sym in symbols1:
    exp = asset_wt_tot[sym][-1] * 100
    print 'Weight %s:' %sym + ' %.2f' %exp + '%'
exp_shy = shy_wt.ix[-1] * 100
print 'Weight SHY: %.2f' %exp_shy + '%'

