"""
 Author: Param Deshpande
 Date created:  Fri Jul 10 23:48:41 IST 2020
 Description: 
 plots individual piecewise  spline curves according to the timestamps in the splineCoeffs.txt
 License :
 ------------------------------------------------------------
 "THE BEERWARE LICENSE" (Revision 42):
 Param Deshpande wrote this code. As long as you retain this 
 notice, you can do whatever you want with this stuff. If we
 meet someday, and you think this stuff is worth it, you can
 buy me a beer in return.
 ------------------------------------------------------------
 date modified:  Fri Jul 10 23:48:41 IST 2020
"""

#import 
#import 
import matplotlib.pyplot as plt
#%matplotlib inline
import numpy as np 
import statistics
import Polynomial as poly
import scipy
from scipy.interpolate import BSpline, splev, splrep, PPoly
#if __name__ == '__main__':
  #import 
  #import 

""" WRITE YOUR FUNCTIONS HERE """

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
  data = np.genfromtxt("splineCoeffs.txt", delimiter=",", names=["time","coeffa" ,"coeffb","coeffc" , "coeffd" ])
  #BUFFERSIZE = 15
  #dataBuffer = [0]*BUFFERSIZE
  #print(type(data))

  #p = poly.Polynomial(4, 0, -4, 3, 0)
  #print(p)
  
  totalTime = data["time"][-1] - data["time"][0]

  for i in range(len(data["time"])):
    currentTimeStamp = data["time"][i]/totalTime
    
    a = data["coeffa"][i]
    b = data["coeffb"][i]
    c = data["coeffc"][i]
    d = data["coeffd"][i]

    if(i != (len(data["time"]) - 1)):
      nextTimeStamp = data["time"][i+1]/totalTime
      p = poly.Polynomial(d, c, b, a)
      X = np.linspace(currentTimeStamp,nextTimeStamp , 200, endpoint=True)
      F = p(X)
      print("x[0] is " + str(X[0]*totalTime) + "F value is " + str(F[0]))
      plt.plot(X, F, label="This is itself a piecewise spline")


  #plt.plot(X, F_derivative, label="F_der")
  y2 = [0, 3, 1, 2, 3, 5, 8, 13, 17, 24]
  x2 = np.linspace(0, 1, 10)

  y3 = [1,7,3,4,10,2]
  x3 = list(range(1,7))
  tck = splrep(x2, y2)
  print( " len of knots is " + str(len(tck[0])))
  print( " len of coeffs is " + str(len(tck[1])))
  print( " degree of Bspline is " + str((tck[2])))

  Bspl = BSpline(tck[0],tck[1],tck[2])
  By2 = Bspl(x2)
  print( " len of bspline is " + str(len(By2)))
  print("  knots / nodes are " + str(tck[0]))
  plt.plot(x2, y2,'o', label=" Y output passed")
  knotx =list(range(0,len(tck[0])))
  knotx[:] = (x/len(tck[0]) for x in knotx)
  plt.plot(knotx , tck[0], 'gs', label="Nodes or knots")
  plt.plot(x2, By2, label="Bspline curve ")

  plt.legend()
  plt.show()

""" END OF FILE """

