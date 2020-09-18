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
import statistics



#if __name__ == '__main__':
  #import 
  #import 

""" WRITE YOUR FUNCTIONS HERE """

def madFilter(dataArr, threshold =3):
  """
  (list),(float) -> (float)
  Description: Calculate of the last point is an outlier depending on the threshold among the given set of points and returns the value that  should be replaced if it is an outlier. 
  >>> sampleVal = madFilter([5,4,4,4,4,5,3,3,1,1,2,2,5])
  >>> sampleVal
  5
  """
  bArr = []
  medianVal = statistics.median(dataArr)
  for element in dataArr:
    bArr.append(abs(medianVal - element))
  madValue =  statistics.median(bArr)
  if(bArr[-1] > threshold*madValue):
    return medianVal
  else :
    return dataArr[-1]


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
  import doctest
  doctest.testmod()
  
  data = np.genfromtxt("logAngles.txt", delimiter=",", names=["date&time","raw_pitch","filter_pitch","raw_yaw" ,"filter_yaw", ])
  BUFFERSIZE = 15
  dataBuffer = [0]*BUFFERSIZE
  print(type(data))

  plt.figure()
  plt.subplot(311)
  plt.plot(data['raw_pitch'], label=" Raw Data ")

  plt.subplot(312)
  plt.plot(data['filter_pitch'], label=" Filtered Data ")
  #plt.label("Filtered yaw")
  
  plt.legend()
  plt.show()
    
  plt.figure()
  plt.subplot(311)
  plt.plot(data['raw_yaw'], label=" Raw Data ")

  plt.subplot(312)
  plt.plot(data['filter_yaw'], label=" Filtered Data ")
  #plt.label("Filtered yaw")
  
  plt.legend()
  plt.show()
  
  
""" END OF FILE """

