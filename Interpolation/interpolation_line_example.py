'''
Created on April 30, 2014

@author: Steven E. Sommer
@summary: Python script to define X and Y values and to interpolate a Y values
for a given values of X to produce an interpolated line. Employs scipy.interpolate.
'''

# Imports
from scipy.interpolate import interp1d
import numpy as np
import matplotlib.pyplot as plt

# Define X and Y values
x = np.arange(0, 10)
y = np.array([3.0,-4.0,-2.0,-1.0, 3.0, 6.0, 10.0, 8.0, 12.0, 20.0])

# Define scipy interpolate function
f = interp1d(x, y, kind = 'cubic')

# Define range of X values for which to interpolate Y values (Result=line)
xint = np.arange(0,9.01,0.01)
yint = f(xint)

# Plot given values for X and Y and plot values for xint and yint
plt.plot(x, y, 'o', c = 'b')
plt.plot(xint, yint,'-r')
plt.show()
