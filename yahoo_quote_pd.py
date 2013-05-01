
'''
Created 4/30/2013

@author: Steven Sommer
@commentary: Script to read Yahoo Finance Data directly to a Pandas DataFrame
'''

import numpy as np
import datetime as dt
import urllib
import urllib2
import time

from zipfile import ZipFile
#from pandas.util.py3compat import StringIO, BytesIO, bytes_to_str

from pandas import DataFrame, read_csv, concat
from pandas.io.parsers import TextParser

def get_quote_yahoo(symbols):
    """
    Get current yahoo quote

    Returns a DataFrame
    """
    if not isinstance(symbols, list):
        raise TypeError, "symbols must be a list"
    # for codes see: http://www.gummy-stuff.org/Yahoo-data.htm
    codes = {'symbol':'s','last':'l1','change_pct':'p2','PE':'r','time':'t1','short_ratio':'s7'}
    request = str.join('',codes.values()) # code request string
    header = codes.keys()

    data = dict(zip(codes.keys(), [[] for i in range(len(codes))]))

    urlStr = 'http://finance.yahoo.com/d/quotes.csv?s=%s&f=%s' % (str.join('+',symbols), request)

    try:
        lines = urllib2.urlopen(urlStr).readlines()
    except Exception, e:
        s = "Failed to download:\n{0}".format(e)
        print s
        return None

    for line in lines:
        fields = line.strip().split(',')
        for i, field in enumerate(fields):
            if field[-2:] == '%"':
                data[header[i]].append(float(field.strip('"%')))
            elif field[0] == '"':
                data[header[i]].append(field.strip('"'))
            else:
                try:
                    data[header[i]].append(float(field))
                except ValueError:
                    data[header[i]].append(np.nan)

    idx = data.pop('symbol')

    return DataFrame(data, index=idx)

#################################################
##############  MAIN CODE  ######################
#################################################


symbols = ['GOOG', 'SPY', 'IBM', 'MSFT', '$SPX']

DataFrame = get_quote_yahoo(symbols)

print DataFrame
