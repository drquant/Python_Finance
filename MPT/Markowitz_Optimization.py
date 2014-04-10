'''
Created on April 10, 2014

@author: Steven E. Sommer
@summary: Python script to call functions from MarkowitzPortfolio.py and calculate MPT characteristics of a given 
portfolio and weights and create a Markowitz plot of given portfolio vs the Efficient Frontier.
Please note that this script requires MarkowitzPortfolio.py in the same folder to run.
'''

# Imports
from MarkowitzPortfolio import *

# Create Portfolio of stock Tickers and weights for each Ticker
stockNames = ["MSFT", "HPQ", "AAPL", "NOK"]
weights = [0.1,0.1,0.7,0.1]
myPortfolio = MarkowitzPortfolio("01/01/2005", "today", "monthly", stockNames, weights, 100000)

print "Portfolio Mean Returns" + "\n"
print myPortfolio.meanReturns 

print "\n" + "\n" + "Portfolio Variance Covariance Matrix" + "\n"
print myPortfolio.varianceCovarianceReturns

print "\n" + "\n" + "Portfolio Expected Return and Variance" + "\n"
print myPortfolio.estimate

print "\n" + "\n" + "Optimum Weights for Same Expected Return and Lowest Variance" + "\n"
print myPortfolio.minimumVarianceWeights

print "\n" + "\n" + "Optimum Weights for Lowest Variance Portfolio" + "\n"
print myPortfolio.globalMinimumVariance

print "\n" + "\n" + "Weights for Minimum Variance Portfolio with Target Return = 0.2" + "\n"
print myPortfolio.ComputeMinVariance(0.2)

print "\n" + "\n" + "5% Value at Risk (VaR) = ", myPortfolio.VaR(0.05)

print "\n" + "\n" + "Creating Markowitz Plot and saving to a PDF file" + "\n"
myPortfolio.plot()
