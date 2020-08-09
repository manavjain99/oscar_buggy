import matplotlib.pyplot as plt
#%matplotlib inline
import numpy as np 
import scipy
from scipy.interpolate import CubicSpline


def getBsplineCoeffs(y):
  """
  (np.array) -> (np.array)
  Description: Input a np.array of vectors, will smoothen it out and generate a spline to give np.array of subsequent coeffs(ie a list of 4 vals abcd).  
  Each list has a sublist of coeffs ie op = [c1,c2,c3,c4,c5 ... ]
  where each cx = np.arary([ax,bx,cx,dx])
  where y val = a +b*x + c*x**2 + d*x**3 
  >>>
  
  """
  #assert (type(y) == list or  ), 'y needs to be a single dim list'
  # the values of x are insignifacant coz we are outputting coeffs, its just that deltax should be same always value ie equidistant . 
  x = np.linspace(0, len(y), len(y))
  cs = CubicSpline(x,y,bc_type='natural')
  coeffs = cs.c
  return np.array(coeffs)

if __name__ == '__main__':
    x0 = np.linspace(0,1,50)
    y0 = np.array(12*x0**0 + x0 + x0**3)

    x1 =  np.linspace(1,2,50)
    y1 = np.array(14*x1**0 + 4*(x1 -1) + 3*(x1-1)**2 + (x1-1)**3) 

    t  = np.linspace(2,3,50)
    x = t-2 
    y2 = 22 + 13*x + 6*x**2 + (-2)*x**3
    plt.plot(x0, y0, label="0 to 1")
    plt.plot(x1, y1, label="1 to 2")
    plt.plot(t, y2, label="2 to 3")

    t=np.linspace(3,4,50)
    x = t-3
    y = 39 + 19*x 
    plt.plot(t, y, label="3 to 4")

    t=np.linspace(4,5,50)
    x = t-4
    y = 58 + 20*x 
    plt.plot(t, y, label="4 to 5")
    
    plt.legend()
    plt.show()

    """
    12.0, 1.0000000000000002, -2.220446049250313e-16, 1.0, 
    14.0, 3.9999999999999996, 3.0, 1.0, 
    22.0, 13.000000000000002, 5.999999999999998, -2.0, 
    39.0, 19.0, 0.0, 0.0, 
    58.0, 19.0, 0.0, 0.0, 
    """