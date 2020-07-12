"""
 Author: Param Deshpande
 Date created:  Fri Jul 10 23:48:41 IST 2020
 Description: 
 plots individual spline curves according to the timestamps in the splineCoeffs.txt
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
import numpy as np 
import statistics
import Polynomial as poly
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

def p(x):
    return x**4 - 4*x**2 + 3*x


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

  p = poly.Polynomial(4, 0, -4, 3, 0)
  print(p)
  prevTimeStamp = 0
  for t,a,b,c,d in zip( data["time"],data["coeffa"],data["coeffb"],data["coeffc"],data["coeffd"]):
    print(str(a) + ',' +str(b) + ',' +str(c) + ',' + str(d) + ',')
    p = poly.Polynomial(d, c, b, a)
    X = np.linspace(prevTimeStamp, t, 50, endpoint=True)
    prevTimeStamp = t
    F = p(X)
    plt.plot(X, F, label="F")

    #F_derivative = p_der(X)
    
    pass

  #plt.plot(X, F_derivative, label="F_der")

  plt.legend()
  plt.show()
    
""" END OF FILE """

