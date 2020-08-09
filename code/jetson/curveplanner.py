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
from scipy.interpolate import splev, splrep, PPoly, CubicSpline
#import 

#if __name__ == '__main__':
  #import 
  #import 

""" WRITE YOUR FUNCTIONS HERE """

def getBsplineCoeffs(y):
  """
  (np.array) -> (np.array)
  Description: Input a np.array of vectors, will smoothen it out and generate a piecewise set of splines coeff format dcba
  ie [[dcba0], [dcba1], [dcba2], ....] 
  where y val = a +b*x + c*x**2 + d*x**3 
  >>>
  
  """
  #assert (type(y) == list or  ), 'y needs to be a single dim list'
  # the values of x are insignifacant coz we are outputting coeffs, its just that deltax should be same always value ie equidistant . 
  x = np.linspace(0, len(y), len(y))
  cs = CubicSpline(x,y,bc_type='natural')
  set_of_coeffs = cs.c  # list of [ [alld], [allc], ... ]
  piecewise_coeffs = []
  for d,c,b,a in zip(set_of_coeffs[0],set_of_coeffs[1],set_of_coeffs[2],set_of_coeffs[3]):
      piecewise_coeffs.append([d,c,b,a])
  return np.array(piecewise_coeffs)


def trajectoryGen(centerXY, newXY, numpts = 3):
  """
  (tup size2, tup size2, int) -> (list of 3 ints list)
  Description:generates linear trajectory for delta gimbal <s, 
  """

  trajList = []
  
  # make sure to negate the vals as axis / coords are inverted wtro gimbal.

  delYaw   = -(newXY[0] - centerXY[0])/(PIX_PER_DEG+PIX_PER_DEG_VAR)
  delPitch = -(newXY[1] - centerXY[1])/(PIX_PER_DEG+PIX_PER_DEG_VAR)
  
  # if less than min of (th% of max <s change or default).
  # if less than min of (th% of max <s change or default).
  if(abs(delYaw) < min(CHANGE_YAW_THOLD,THRES_PERCENT_CHANGE*MAX_DEL_YAW)):
    delYaw = 0

  if(abs(delPitch) < min(CHANGE_PITCH_THOLD,THRES_PERCENT_CHANGE*MAX_DEL_PITCH)):
    delPitch = 0
    # S1 linearly diving pts from 0 to del<s as roll pitch yaw 
  
  if((newXY[0] != -1) and (newXY[1] != -1)):
    #if delYaw , delPitch greater than angle threshold.
    for i in range(numpts):
      trajList.append([0, i*delPitch/(numpts-1), i*delYaw/(numpts-1)])

  # if no obj detected.
  else:
    for i in range(numpts):
      trajList.append([0, 0, 0])


  return trajList


def spline6pt(y):
  """
  (np.array[] (size = 6) ) -> (list[4])
  Description: Generates peicewise spline curves for the 6 y pts, with x pts equally spaced as x[0:5].
  Outputs the coeffs last piecewise curves ie coeffnew. ie ( coeffx = ax, bx, cx, dx)
  regenrate the splines example ( for ref of abcd ignore rest) 
  y = a2 + b2*(x-2) + c2*(x-2)**2 + d2*(x-2)**3
  
  Similarly for coeff 3 for x betn 3,4 as 
  y = a3 + b3*(x-3) + c3*(x-3)**2 + d3*(x-3)**3
  >>>
  """
  # if a valid entry 
  if( y.size == 6):
    #logging.info("reached spline 6pt")
    x = np.array([0, 1, 2, 3, 4, 5])
    cs = CubicSpline(x,y,bc_type='natural')

    # Polynomial coefficients for 4 < x <= 5 ie the last curve among 6 pts.
    a4 = cs.c.item(3,4)
    b4 = cs.c.item(2,4)
    c4 = cs.c.item(1,4)
    d4 = cs.c.item(0,4)

    coeff4 = [a4, b4 , c4, d4 ]
    #logging.info(str(coeff4))
    return coeff4


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
  #x = np.linspace(0, 10, 10)
  x = list(range(0,8))
  y = [10,20, 35, 45, 55, 70,82,94]
  #print(x[:9])
  #y = [0, 3, 1, 2, 3, 5, 8, 13, 17, 24]
  print(getBsplineCoeffs(y))
  
  
  
""" END OF FILE """

'''


 [-1.53163159e+00  7.16537081e+00  2.56150319e+00  1.00000000e+01]
 [ 9.58939207e-01 -3.33724581e+00  1.13115032e+01  3.50000000e+01]
 [ 1.04548414e+00 -4.94542464e-02  7.44098884e+00  4.50000000e+01]
 [-1.79126639e+00  3.53506280e+00  1.14245415e+01  5.50000000e+01]
 [ 7.60206402e-01 -2.60642195e+00  1.24858453e+01  7.00000000e+01]
 [ 7.60206402e-01  2.60642195e+00  1.24858453e+01  9.40000000e+01]





[0.         1.11111111 2.22222222 3.33333333 4.44444444]
[[ 1.36893061e+00 -6.58810203e+00  8.33007558e+00 -5.16398318e-17]
 [ 1.36893061e+00 -6.58810203e+00  8.33007558e+00 -5.16398318e-17]
 [ 1.36893061e+00 -6.58810203e+00  8.33007558e+00 -5.16398318e-17]
 [ 1.36893061e+00 -6.58810203e+00  8.33007558e+00 -5.16398318e-17]
 [-1.01265304e+00  2.53810203e+00 -6.69924425e-01  1.00000000e+00]
 [ 4.94681553e-01 -8.37408107e-01  1.21973549e+00  2.00000000e+00]
 [-2.37073171e-01  8.11530402e-01  1.19098248e+00  3.00000000e+00]
 [ 4.53611130e-01  2.12864995e-02  2.11633459e+00  5.00000000e+00]
 [-8.48371350e-01  1.53332360e+00  3.84367915e+00  8.00000000e+00]
 [ 7.52874270e-01 -1.29458090e+00  4.10894881e+00  1.30000000e+01]
 [ 7.52874270e-01  3.72458090e+00  9.50894881e+00  2.40000000e+01]
 [ 7.52874270e-01  3.72458090e+00  9.50894881e+00  2.40000000e+01]
 [ 7.52874270e-01  3.72458090e+00  9.50894881e+00  2.40000000e+01]]
'''