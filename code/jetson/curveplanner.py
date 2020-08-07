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
from scipy.interpolate import splev, splrep
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
  assert (type(y) == list), 'y needs to be a single dim list'
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
  
  
  
  
""" END OF FILE """

