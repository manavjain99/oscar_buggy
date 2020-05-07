"""
 Author: Param Deshpande
 Date created:  Sun 26 Apr 13:28:45 IST 2020
 Description: 
 test
 License :
 ------------------------------------------------------------
 "THE BEERWARE LICENSE" (Revision 42):
 Param Deshpande wrote this code. As long as you retain this 
 notice, you can do whatever you want with this stuff. If we
 meet someday, and you think this stuff is worth it, you can
 buy me a beer in return.
 ------------------------------------------------------------
 date modified:  Sun 26 Apr 13:28:45 IST 2020

"""

#import 
#import 

if __name__ == '__main__':
    pass
    import logging
    import greenBallTracker as GBT
    from collections import deque
    from imutils.video import VideoStream
    import numpy as np
    import argparse
    import cv2
    import imutils
    import time

""" WRITE YOUR FUNCTIONS HERE """

PIX_PER_DEG = 18.0
PIX_PER_DEG_VAR = 1.3

def trajectoryGen(prevXY, newXY, numpts = 6):
  """
  (tup size2, tup size2, int) -> (list of 3 ints list)
  Description:generates trajectory for delta gimbal <s, 
  """
  trajList = list()
  delYaw = (newXY[0] - prevXY[0])/(PIX_PER_DEG+PIX_PER_DEG_VAR)
  delPitch = (newXY[1] - prevXY[1])/(PIX_PER_DEG+PIX_PER_DEG_VAR)
  
  # S1 linearly diving pts from 0 to del<s as roll pitch yaw 
  for i in range(numpts):
    trajList.append([0, i*delPitch/(numpts-1), i*delYaw/(numpts-1)])

  return trajList


""" START YOUR CODE HERE """

if __name__== '__main__':
    
    pass    
    #vs = VideoStream(src=0).start()
    # allow the camera or video file to warm up
    time.sleep(3.0)
    objA = 10
    objCX = 0
    objCY = 0
    trajList = trajectoryGen((0,0), (180,180))
    print(trajList)
    
    #frame = vs.read()
    #while(1):
    #    frame = vs.read()
    #    objA, objCX, objCY = GBT.trackGreenBall(frame)
    #    print(str(objA) + " " +str(objCX) + " " +str(objCY))
    #    if(objA == -1):
    #        vs.stop()
    #        vs.release()

#import doctest
#doctest.testmod()




""" END OF FILE """

