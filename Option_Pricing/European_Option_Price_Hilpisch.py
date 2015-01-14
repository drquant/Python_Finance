'''
Created 1/14/2015

@author: Steven E. Sommer, MD, MBA. Adapted from Hilpisch
@summary:
Valuation of European Call and Put Options
Under Stochastic Volatility and Interest Rates
Parameter Examples from Medvedev & Scaillet ( 2009 ):
" Pricing American Options Under Stochastic Volatility
  and Stochastic Interest Rates "
  Working Paper No. 429 , Finrisk --- MS ( 2009 )

(c) Visixion GmbH - Dr. Y. Hilpisch
Script for illustration purposes only .
August 2011

SVSI_Euro_Valuation.py
'''

# Imports
from numpy import *
from scipy.integrate import *

#
# Example Parameters H93 Model
#
kappa_v = 1.5
theta_v = 0.02
sigma_v = 0.15
rho     = 0.1
v0      = 0.01
S0      = 100.0
K       = 90.0
T       = 1.0/12

#
# Valuation by Integration
#
def H93_Value_Call_Int ( S0 ,K ,T , B0T , kappa_v , theta_v , sigma_v , rho , v0 ):
    r=- log ( B0T )/ T
    Int = quad ( lambda u: H93_Int_Func (u ,S0 ,K ,T ,r , kappa_v ,
                           theta_v , sigma_v , rho , v0 ),0 , 1000 )[ 0 ]
    return max(0 ,S0 - B0T * sqrt ( S0 *K )/ pi * Int )

#
# Integration Function
#
def H93_Int_Func (u ,S0 ,K ,T ,r , kappa_v , theta_v , sigma_v , rho , v0 ):
    CF = H93_Char_Func (u - 1j *0.5 ,T ,r , kappa_v , theta_v , sigma_v , rho , v0 )
    return 1 /( u ** 2+ 0.25 )*( exp ( 1j * u* log ( S0 /K ))* CF ). real

#
# Characteristic Function
#
def H93_Char_Func (u ,T ,r , kappa_v , theta_v , sigma_v , rho , v0 ):
    c1 = kappa_v * theta_v
    c2 = - sqrt (( rho * sigma_v *u* 1j - kappa_v )** 2 - sigma_v ** 2 *( - u*1j - u ** 2 ))
    c3 = ( kappa_v - rho * sigma_v * u* 1j + c2 )/( kappa_v - rho * sigma_v *u*1j - c2 )
    H1 = (r* u* 1j *T +( c1 / sigma_v ** 2 )*(( kappa_v - rho * sigma_v *u * 1j + c2 )* T
                               -2 * log ((1 - c3 * exp ( c2 * T ))/( 1 - c3 ))))
    H2 = (( kappa_v - rho * sigma_v *u* 1j + c2 )/ sigma_v ** 2*
         ((1 - exp ( c2 * T ))/( 1 - c3 * exp ( c2 *T ))))
    return exp ( H1 + H2 * v0 )

#
# Example Parameters CIR85 Model
#
kappa_r , theta_r , sigma_r , r0 ,T =0.3 , 0.04 , 0.1 , 0.04 , 1.0/ 12

#
# (Zero - Coupon -) Bond Valuation Formula
#
def gamma ( kappa_r , sigma_r ):
    return sqrt ( kappa_r ** 2+2* sigma_r ** 2)

def b1( alpha ):
    kappa_r , theta_r , sigma_r , r0 ,T = alpha
    g = gamma ( kappa_r , sigma_r )
    return (( 2* g* exp (( kappa_r +g )* T/2 ))/
            (2* g +( kappa_r +g )*( exp ( g*T) -1 )))**( 2* kappa_r * theta_r / sigma_r ** 2)

def b2( alpha ):
    kappa_r , theta_r , sigma_r , r0 ,T = alpha
    g = gamma ( kappa_r , sigma_r )
    return (( 2 *( exp (g*T) -1 ))/
            (2* g +( kappa_r +g )*( exp ( g*T) -1 )))

def B( alpha ):
    b_1 = b1 ( alpha ); b_2 = b2 ( alpha )
    kappa_r , theta_r , sigma_r , r0 ,T = alpha
    return b_1 * exp ( - b_2 * r0 )

#
# Example Values
#
B0T =B ([ kappa_r , theta_r , sigma_r ,r0 , T ]) # Discount Factor
C0 = H93_Value_Call_Int (S0 ,K ,T , B0T , kappa_v , theta_v , sigma_v , rho , v0 )
P0 = C0 + K* B0T - S0
print " H93 Call Value = ", C0
print " H93 Put Value  = ", P0
