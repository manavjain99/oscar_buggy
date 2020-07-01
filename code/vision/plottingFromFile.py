"""
 Author: Param Deshpande
 Date created:  Wed Jul 1 16:44:42 IST 2020
 Description: 
 Plots a graph for a csv file
 License :
 ------------------------------------------------------------
 "THE BEERWARE LICENSE" (Revision 42):
 Param Deshpande wrote this code. As long as you retain this 
 notice, you can do whatever you want with this stuff. If we
 meet someday, and you think this stuff is worth it, you can
 buy me a beer in return.
 ------------------------------------------------------------
 date modified:  Wed Jul 1 16:44:42 IST 2020
"""

#import 
#import 
import matplotlib.pyplot as plt
import numpy as np 
data = np.genfromtxt("logAngles.txt", delimiter=",", names=["date&time", "yaw", "pitch"])


plt.figure()
plt.subplot(211)
plt.plot(data['yaw'])

plt.subplot(212)
plt.plot(data['pitch'])
plt.show()

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
  
  
  
  
""" END OF FILE """

