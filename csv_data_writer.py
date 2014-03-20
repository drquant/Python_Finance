'''
Created March 19. 2014

@author: Steven E. Sommer
@summary: Python script to download stock price and volume data for a list of
ticker symbols from Yahoo Finance into a PANDAS DataFrame and write the
timestamped price and volume data to a csv file. This is a very nice way to
quickly create csv data files from a list of ticker symbols.
'''

# Imports
import pandas.io.data as web
import datetime as dt
import csv

# Specify starting and ending dates for the data files
startdate = dt.datetime(2007,1,1)
enddate = dt.datetime(2014,3,18)

# Specify the list of ticker symbols to download
symbols = ['SPY','IWM']

# Acquire data from Yahoo Finance
print "Getting data from Yahoo Finance"
# Loop through the symbol list downloading data to PANDAS and writing this
# data to a csv file
for sym in symbols:
    # Download the data to PANDAS
    sym1 = web.DataReader(sym,'yahoo',startdate,enddate)
    print "Data for " + sym
    print sym1
    
    # Write data to a csv file
    print "Writing data to csv file"
    with open('%s.csv' %sym, 'w') as outfile:
        writer = csv.writer(outfile)
        for index in sym1.index:
            writer.writerow([index, sym1['Open'][index], sym1['High'][index], sym1['Low'][index],sym1['Close'][index], sym1['Volume'][index], sym1['Adj Close'][index]])
