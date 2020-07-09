"""
 Author: Param Deshpande
 Date created:  Wed 6 May 21:28:52 IST 2020
 Description: 
 processes to track a given green ball.
 License :
 ------------------------------------------------------------
 "THE BEERWARE LICENSE" (Revision 42):
 Param Deshpande wrote this code. As long as you retain this 
 notice, you can do whatever you want with this stuff. If we
 meet someday, and you think this stuff is worth it, you can
 buy me a beer in return.
 ------------------------------------------------------------
 date modified:  Wed 6 May 21:28:52 IST 2020
"""

#import 
#import 
from collections import deque
from imutils.video import VideoStream
import numpy as np
import argparse
import cv2
import imutils
import time



if __name__ == '__main__':
  pass


  #import queue 
  #import 

""" WRITE YOUR FUNCTIONS HERE """

greenLower = (29, 86, 6)
greenUpper = (64, 255, 255)

# default as it hasn't been used yet.
#objCenterX =0
#objCenterY =0
#objArea = 0


def trackGreenBall(frame):
  """
  (image) -> (float, float, float)
  Description: Tracks the green ball returns its area, objCenterX, objCenterY
  >>>

  """
  objCenterX =-1
  objCenterY =-1
  objArea   = -1

  #blue color
  #greenLower = (51,51,0)
  #greenUpper = (255,255,204)

  # green color.
  greenLower = (29, 86, 6)
  greenUpper = (64, 255, 255)

  frame = imutils.resize(frame, width=600)
  blurred = cv2.GaussianBlur(frame, (11, 11), 0)
  hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
  # construct a mask for the color "green", then perform
  # a series of dilations and erosions to remove any small
  # blobs left in the mask
  mask = cv2.inRange(hsv, greenLower, greenUpper)
  mask = cv2.erode(mask, None, iterations=2)
  mask = cv2.dilate(mask, None, iterations=2)

      # find contours in the mask and initialize the current
  # (x, y) center of the ball
  cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
    cv2.CHAIN_APPROX_SIMPLE)
  cnts = imutils.grab_contours(cnts)
  center = None
  # only proceed if at least one contour was found
  if len(cnts) > 0:
    # find the largest contour in the mask, then use
    # it to compute the minimum enclosing circle and
    # centroid
    c = max(cnts, key=cv2.contourArea)
    ((x, y), radius) = cv2.minEnclosingCircle(c)
    M = cv2.moments(c)
    center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
    # only proceed if the radius meets a minimum size
    if radius > 10:
      # draw the circle and centroid on the frame,
      # then update the list of tracked points
      cv2.circle(frame, (int(x), int(y)), int(radius),
        (0, 255, 255), 2)
      cv2.circle(frame, center, 5, (0, 0, 255), -1)
    if((center) == None):
      objCenterX = -1
      objCenterY = -1
      objArea = -1
    else :
      objCenterX = center[0]
      objCenterY = center[1]
      objArea = 1


  return objArea, objCenterX, objCenterY





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
  vs = VideoStream(src=0).start()
  #vs = cv2.VideoCapture('ball_tracking_example.mp4')
  # allow the camera or video file to warm up
  time.sleep(3.0)
  objCX = 0
  objCY = 0
  while(1):
    ret, frame = vs.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    objA, objCX, objCY = trackGreenBall(frame)
    print(str(objA) + ", " +str(objCX) + ", " +str(objCY))

    cv2.imshow('frame',gray)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

  cap.release()
  cv2.destroyAllWindows()

  #frame = vs.read()
  while(1):
    frame = vs.read()
  
  #import doctest
  #doctest.testmod()
  
  
  
  
""" END OF FILE """

