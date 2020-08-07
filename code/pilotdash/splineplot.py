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
  
  plt.plot(x2, y2,'-o')
  plt.legend()
  plt.show()

""" END OF FILE """

