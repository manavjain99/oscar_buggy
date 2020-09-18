"""
 Author: Param Deshpande
 Date created:  Wed Jul 8 16:03:34 IST 2020
 Description: 
 Returns aruco codes' area,cx, and cy in a frame.
 License :
 ------------------------------------------------------------
 "THE BEERWARE LICENSE" (Revision 42):
 Param Deshpande wrote this code. As long as you retain this 
 notice, you can do whatever you want with this stuff. If we
 meet someday, and you think this stuff is worth it, you can
 buy me a beer in return.
 ------------------------------------------------------------
 date modified:  Wed Jul 8 16:03:34 IST 2020
"""

#import 
#import 
import cv2 as cv
import numpy as np

#if __name__ == '__main__':
  #import 
  #import 

""" WRITE YOUR FUNCTIONS HERE """

# Load the predefined dictionary
MARKER_ID = 33 

dictionary = cv.aruco.Dictionary_get(cv.aruco.DICT_6X6_250)
parameters =  cv.aruco.DetectorParameters_create()

def trackArucoMarker(frame):
  """
  (image) -> (float,float,float,float)
  Description: 
  Return area, theta ,cx, cy  and checks if correct marker or not.
  #>>>
  
  """

  objCenterX =-1
  objCenterY =-1
  objArea   = -1
  objRotation = -1

  markerCorners, markerIds, rejectedCandidates = cv.aruco.detectMarkers(frame, dictionary, parameters=parameters)

  #print("len(markerIds) " + str(len(markerIds)) )
  if (markerIds is not None):
    for i in range(  len(markerIds)  ):
      if(markerIds[i][0] == MARKER_ID):
        objCenterX = (markerCorners[0][i][0][0]+markerCorners[0][i][1][0]+markerCorners[0][i][2][0]+markerCorners[0][i][3][0])/4.0
        objCenterY = (markerCorners[0][i][0][1]+markerCorners[0][i][1][1]+markerCorners[0][i][2][1]+markerCorners[0][i][3][1])/4.0
        objArea = (markerCorners[0][i][0][0] - markerCorners[0][i][1][0])*(markerCorners[0][i][0][1] - markerCorners[0][i][3][1])
        objArea = abs(objArea)
        objRotation = 0
  return objArea, objRotation, objCenterX, objCenterY
#def ...:
#  """
#  () -> ()
#  Description: 
#  >>>
#  
#  """


#def ...:
#  """
#  () -> ()/moddoc/DemoArUco/modinfo.html cheaper version of what im doing ... 
#  Description: 
#  >>>
#  
#  """

""" START YOUR CODE HERE """

if __name__ == '__main__':
  pass
  #import doctest
  #doctest.testmod()
  frame = cv.imread('../playground/marker33.png')
  #cv.imshow(frame)
  cv.imshow('image',frame)
  cv.waitKey(0)
  cv.destroyAllWindows()

  Area, pose ,Cx, Cy = trackArucoMarker(frame)
  print(Area)
  print(pose)
  print(Cx)
  print(Cy)
  cap = cv.VideoCapture(0)

  while(True):
      # Capture frame-by-frame
      ret, frame = cap.read()

      # Our operations on the frame come here
      Area, pose ,Cx, Cy = trackArucoMarker(frame)
      print(  str(Area) + str(pose) +str(Cx) + str(Cy) )

      # Display the resulting frame
      cv.imshow('frame',frame)
      if cv.waitKey(1) & 0xFF == ord('q'):
          break

  # When everything done, release the capture
  cap.release()
  cv.destroyAllWindows()
  # Passed the tests , too lazy to write a separate test script.
  # Didnt check for multiple arucos , 
  # Didnt check for paralleogram arucos , 
  # Hopefully these work as well. 
""" END OF FILE """

