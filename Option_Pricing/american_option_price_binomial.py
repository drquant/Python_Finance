'''
Created 1/13/2015

@author: Steven E. Sommer, MD, MBA
@summary: Python implementation of the American binomial option pricing model.
'''

# Imports
import numpy as np
import math

# Define the function for the Binomial American Stock Option
def binomial_am_stock_opt(S0, K, r, T, N, pu, pd, is_call_opt=True, div=0.):
    '''
    Price an American option by the binomial tree model.
    
    S0 - current stock price
    K - strike price of option
    r - annualized risk-free rate in decimal point form
    T - time left to maturity in years
    N - number of steps in the binomial tree
    pu - probability of up state in decimal point form
    pd - probability of down state in decimal point form
    is_call_opt - True for a call option; False for a put option
    div - annualized dividend yield of the stock in decimal point form
    '''
    N = max(1, N)
    M = N+1
    u = 1 + pu
    d = 1 - pd
    dt = T/N
    discount_factor = math.exp(-(r-div)*dt)
    qu = (math.exp((r-div)*dt)-d)/(u-d) 
    qd = 1-qu

    STs = [np.array([S0])]
    for i in range(N):
        prev_branches = STs[-1]
        st = np.concatenate((prev_branches*u, [prev_branches[-1]*d]))
        STs.append(st)
    
    ''' Get terminal payoffs '''
    payoffs = np.maximum(0, (STs[N]-K)if is_call_opt else(K-STs[N]))

    for i in reversed(range(N)):  
        early_ex_payoff = (STs[i] - K) if is_call_opt else (K - STs[i])
        rn_payoff = (payoffs[:-1]*qu + payoffs[1:]*qd)*discount_factor
        payoffs = np.maximum(rn_payoff, early_ex_payoff)

    return payoffs[0]

##################################################################################
##############################  MAIN Code  #######################################
##################################################################################

if __name__ == "__main__":

    # Call the Binomial American Stock Option Pricing Function and pass the required function arguments (variables).

    american_option_price = binomial_am_stock_opt(50, 50, 0.05, 0.5, 2, 0.2, 0.2, False, 0)

    # Print the current American Option Price
    # Print statement to round American Option price to 2 significant digits
    print 'Current American Stock Option Price (Binomial Tree Model) = $ %.2f' % american_option_price 
    # Print statement to print all digits calculated
    print 'Current American Stock Option Price (Binomial Tree Model) = $', american_option_price

