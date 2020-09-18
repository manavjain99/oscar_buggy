import matplotlib.pyplot as plt
#%matplotlib inline
import numpy as np 
import scipy
from scipy.interpolate import CubicSpline


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

if __name__ == '__main__':
    
    y = np.array([1,3,3,0,5,8,7,8,4,0])
    coef = getBsplineCoeffs(y)
    print(coef)
    """
    for i,d,c,b,a in zip(range(len(coef)),coef[0],coef[1],coef[2],coef[3]):
        #for singc in 
        pass
        # printing in d,c,b,a fashion coz thats how python uses convention 
        print(str(i) + str(', ') + str(d)  + str(', ') + str(c) + str(', ') + str(b) + str(',') + str(a) )
    #print()
    
    
    
    
    #
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

    12.0, 1.0000000000000002, -2.220446049250313e-16, 1.0, 
    14.0, 3.9999999999999996, 3.0, 1.0, 
    22.0, 13.000000000000002, 5.999999999999998, -2.0, 
    39.0, 19.0, 0.0, 0.0, 
    58.0, 19.0, 0.0, 0.0, 
    """