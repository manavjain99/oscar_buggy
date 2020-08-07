"""
 Author: Param Deshpande
 Date created:  Fri Aug 7 19:02:05 IST 2020
 Description: 
 Calculates and returns curves / curve parameters for a given set of inputs.
 License :
 ------------------------------------------------------------
 "THE BEERWARE LICENSE" (Revision 42):
 Param Deshpande wrote this code. As long as you retain this 
 notice, you can do whatever you want with this stuff. If we
 meet someday, and you think this stuff is worth it, you can
 buy me a beer in return.
 ------------------------------------------------------------
 date modified:  Fri Aug 7 19:02:05 IST 2020
"""

import scipy
import numpy as np 
from scipy.interpolate import splev, splrep, PPoly
#import 

#if __name__ == '__main__':
  #import 
  #import 

""" WRITE YOUR FUNCTIONS HERE """

def getBsplineCoeffs(y):
  """
  (list) -> (ndim list)
  Description: Input a list of vectors, will smoothen it out and generate a spline to give list of subsequent coeffs(ie a list of 4 vals abcd).  
  where y val = a +b*x + c*x**2 + d*x**3 
  >>>
  
  """
  #assert (type(y) == list or  ), 'y needs to be a single dim list'
  x = np.linspace(0, len(y), len(y))
  tck = splrep(x, y)
  pp = PPoly.from_spline(tck)
  return pp.c.T

#def ...:
#  """
#  () -> ()
#  Description: 
#  >>>
#  
#  """


#def ...:
#  """
#  () -> ()
#  Description: 
#  >>>
#  
#  """

""" START YOUR CODE HERE """

if __name__ == '__main__':
  pass
  #import doctest
  #doctest.testmod()
  x = np.linspace(0, 10, 10)
  y = [0, 3, 1, 2, 3, 5, 8, 13, 17, 24]
  print(getBsplineCoeffs(y))
  
  
  
""" END OF FILE """

'''
1  ,  1.36893061e+00 ,-6.58810203e+00 , 8.33007558e+00 , -5.16398318e-17
2  ,  1.36893061e+00 ,-6.58810203e+00 , 8.33007558e+00 , -5.16398318e-17
3  ,  1.36893061e+00 ,-6.58810203e+00 , 8.33007558e+00 , -5.16398318e-17
4  ,  1.36893061e+00 ,-6.58810203e+00 , 8.33007558e+00 , -5.16398318e-17
5  , -1.01265304e+00 , 2.53810203e+00 ,-6.69924425e-01 ,  1.00000000e+00
6  ,  4.94681553e-01 ,-8.37408107e-01 , 1.21973549e+00 ,  2.00000000e+00
7  , -2.37073171e-01 , 8.11530402e-01 , 1.19098248e+00 ,  3.00000000e+00
8  ,  4.53611130e-01 , 2.12864995e-02 , 2.11633459e+00 ,  5.00000000e+00
9  , -8.48371350e-01 , 1.53332360e+00 , 3.84367915e+00 ,  8.00000000e+00
10 ,  7.52874270e-01 ,-1.29458090e+00 , 4.10894881e+00 ,  1.30000000e+01
11 ,  7.52874270e-01 , 3.72458090e+00 , 9.50894881e+00 ,  2.40000000e+01
12 ,  7.52874270e-01 , 3.72458090e+00 , 9.50894881e+00 ,  2.40000000e+01
13 ,  7.52874270e-01 , 3.72458090e+00 , 9.50894881e+00 ,  2.40000000e+01
'''