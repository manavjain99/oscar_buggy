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
    import queue
""" WRITE YOUR FUNCTIONS HERE """

PIX_PER_DEG = 18.0
PIX_PER_DEG_VAR = 1.3

CHANGE_YAW_THOLD = 2
CHANGE_PITCH_THOLD = 2
THRES_PERCENT_CHANGE =0.10
VID_SRC = 2

FRAME_CX = 460/2
FRAME_CY = 639/2


commQ = queue.Queue(maxsize=3000)


# need not change these vars.
MAX_DEL_YAW = FRAME_CX/(PIX_PER_DEG+PIX_PER_DEG_VAR)
MAX_DEL_PITCH = FRAME_CY/(PIX_PER_DEG+PIX_PER_DEG_VAR)


def trajectoryGen(centerXY, newXY, numpts = 3):
  """
  (tup size2, tup size2, int) -> (list of 3 ints list)
  Description:generates trajectory for delta gimbal <s, 
  """

  trajList = []
  
  # make sure to negate the vals as axis / coords are inverted wtro gimbal.

  delYaw   = -(newXY[0] - centerXY[0])/(PIX_PER_DEG+PIX_PER_DEG_VAR)
  delPitch = -(newXY[1] - centerXY[1])/(PIX_PER_DEG+PIX_PER_DEG_VAR)
  
  # if less than min of (th% of max <s change or default).
  if(abs(delYaw) < min(CHANGE_YAW_THOLD,THRES_PERCENT_CHANGE*MAX_DEL_YAW)):
    delYaw = 0

  if(abs(delPitch) < min(CHANGE_PITCH_THOLD,THRES_PERCENT_CHANGE*MAX_DEL_PITCH)):
    delPitch = 0
  # S1 linearly diving pts from 0 to del<s as roll pitch yaw 
  
  if((newXY[0] is not -1) and (newXY[1] is not -1)):
    #if delYaw , delPitch greater than angle threshold.
    for i in range(numpts):
      trajList.append([0, i*delPitch/(numpts-1), i*delYaw/(numpts-1)])

  # if no obj detected.
  else:
    for i in range(numpts):
      trajList.append([0, 0, 0])


  return trajList


def comms_thread(trajQ = commQ):
  """
  (list) -> (NoneType)
  Description: Sends gimbal traj to mcu and waits for ack.
  >>>
  
  """

  # if there is a new list of trajectory in the Queue. 
  gimbal_coords_buffer = []
  if not trajQ.empty():
    start_time_comms = time.time()
    logging.info("TrajQ size" + str(trajQ.qsize())) # FPS = 1 / time to process loop

    ptTrajList = trajQ.get()
    # start sending vals one by one and wait for ack by mcu.
    for i in range(len(ptTrajList) -1 ):
      gimbal_coords_buffer = []
      gimbal_coords_buffer.append("<"+str(ptTrajList[i][0])+', '+str(ptTrajList[i][1])+', '+str(ptTrajList[i][2])+">")
      #stcom.runTest(gimbal_coords_buffer)
    #logging.info("FPS comms : " + str(1.0 / (time.time() - start_time_comms))) # FPS = 1 / time to process loop

  return gimbal_coords_buffer

""" START YOUR CODE HERE """

if __name__== '__main__':

  format = "%(asctime)s: %(message)s"
  logging.basicConfig(format=format, level=logging.INFO,
                      datefmt="%H:%M:%S")
 
  time.sleep(3.0)
  objA = 10
  objCX = 0
  objCY = 0
  trajList = trajectoryGen((0,0), (180,180))
  print(trajList)
  while(1):

    # assuming i get old and new XY coords 
    
    # I put traj in commsQ
    #commQ.put(trajList)

    # I call comms_thread
    #print(comms_thread())
    break
    # print its o/p