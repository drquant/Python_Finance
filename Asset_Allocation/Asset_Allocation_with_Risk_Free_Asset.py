'''
Created June 26, 2014

@author: Steven E. Sommer
@summary: Asset Allocation for Tangent Portfolio with Risk-Free Asset in Python
Note: Script written to run in Python 2.7.6.
'''

# Adapted from Accelerated Python for Quants Tutorial, Lesson 4
# (c) 2014 QuantAtRisk
 
from numpy import matrix, power
from math import sqrt
 
def TangentPortfolio(m,C,rf):
    # find number of rows and columns for the covariance matrix 
    (nr,nc)=C.shape
    A=matrix([[0.0] for r in xrange(nr)])
    A=(1/C)*(m-rf)
    (nr,nc)=A.shape
    A=A/sum(A[r,0] for r in xrange(nr))
    w=[A[r,0] for r in xrange(nr)]
    pret=mu.T*A
    prsk=power(A.T*(C*A),0.5)
    return matrix(w),pret,prsk

cov=matrix([[0.04, 0.004, 0.02],[0.004, 0.09, 0.09],[0.02,0.09,0.16]])
mu=matrix([[0.13],[0.11],[0.19]])
rf=0.05
 
w,ret,rsk=TangentPortfolio(mu,cov,rf)

print 'Portfolio weights:' + '\n'
print(w.T),'\n'
 
print 'Expected Portfolio Return = ',ret 
print 'Expected Portfolio Risk = ',rsk,'\n'

# Calculate the Sharpe Ratio

sharpe=(ret-rf)/rsk
print 'Sharpe Ratio of 1st Asset = ',sharpe,'\n'

count = 0
for r in xrange(3):
    count = count + 1
    print 'Sharpe Ratio Asset #',count,' = ',((mu[r,0]-rf)/sqrt(cov[r,r]))

# Calculate the Expected Portfolio Return and Expected Risk for fraction of
# capital invested in risky assets

# Define fraction of Capital invested in risky assets
alpha= [0.7,0.25]

# Calculate and print Expected Portfolio Return and Expected Portfolio Risk
count2 = 0
for a in alpha:
    count2 = count2 + 1
    print '\n' + 'Portfolio',count2
    print 'Capital at Risk = ',a
    print 'Expected Portfolio Return = ',((matrix(a)*w)*mu)+(1-a)*rf
    print 'Expected Rate of Risk = ',matrix(a)*power(w*cov*w.T,1),'\n'
