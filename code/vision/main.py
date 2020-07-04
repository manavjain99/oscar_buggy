"""
 Author: Param Deshpande
 Date created:  Mon 27 Apr 18:11:03 IST 2020
 Description: 
 Main jetson/pc python file for controlling gimbal via the tracked object.
 This file sends 3 peicewise spine curves coeff to the MCU @ 3fps.
 
 License :
 ------------------------------------------------------------
 "THE BEERWARE LICENSE" (Revision 42):
 Param Deshpande wrote this code. As long as you retain this 
 notice, you can do whatever you want with this stuff. If we
 meet someday, and you think this stuff is worth it, you can
 buy me a beer in return.
 ------------------------------------------------------------
 date modified:  Mon 27 Apr 18:11:03 IST 2020
"""

#import gimbalcmd
INCLUDE_STM = False
LOG_FILES = True 
CAMERA_AVAIL = False

if __name__ == '__main__':
  import concurrent.futures
  import logging
  import queue
  import random
  import threading
  import serial
  import time
  import cv2
  import greenBallTracker as GBT 
  #import matplotlibLive as MPLive
  if INCLUDE_STM == True:
    import ComArduino2 as stcom
  import numpy as np
  from scipy.interpolate import CubicSpline


""" WRITE YOUR VARIABLES HERE """

NO_OF_PTS = 3

CHANGE_YAW_THOLD = 2
CHANGE_PITCH_THOLD = 2
THRES_PERCENT_CHANGE =0.10
# 3, 2, 1 for ext webcam 0 for webcam
VID_SRC = 0
VIDEO_SOURCE = "ball_tracking_example.mp4"
# ie processing every nth frame.
PROC_FRAME_FREQ = 3

FRAME_CX = 480.0/2.0
FRAME_CY = 640.0/2.0

PIX_PER_DEG = 18.0
PIX_PER_DEG_VAR = 1.3

MAX_NO_FRAMES = 10000

ACK_MCU_MSG = '1'

# need not change these vars.
MAX_DEL_YAW = FRAME_CX/(PIX_PER_DEG+PIX_PER_DEG_VAR)
MAX_DEL_PITCH = FRAME_CY/(PIX_PER_DEG+PIX_PER_DEG_VAR)

# should be equal to t_grab / t_tick_mcu

imageQ = queue.Queue(maxsize=10000)
commQ = queue.Queue(maxsize=30000)

""" WRITE YOUR FUNCTIONS HERE """

def trajectoryGen(centerXY, newXY, numpts = NO_OF_PTS):
  """
  (tup size2, tup size2, int) -> (list of 3 ints list)
  Description:generates linear trajectory for delta gimbal <s, 
  """

  trajList = []
  
  # make sure to negate the vals as axis / coords are inverted wtro gimbal.

  delYaw   = -(newXY[0] - centerXY[0])/(PIX_PER_DEG+PIX_PER_DEG_VAR)
  delPitch = -(newXY[1] - centerXY[1])/(PIX_PER_DEG+PIX_PER_DEG_VAR)
  
  # if less than min of (th% of max <s change or default).
  # if less than min of (th% of max <s change or default).
  if(abs(delYaw) < min(CHANGE_YAW_THOLD,THRES_PERCENT_CHANGE*MAX_DEL_YAW)):
    delYaw = 0

  if(abs(delPitch) < min(CHANGE_PITCH_THOLD,THRES_PERCENT_CHANGE*MAX_DEL_PITCH)):
    delPitch = 0
    # S1 linearly diving pts from 0 to del<s as roll pitch yaw 
  
  if((newXY[0] != -1) and (newXY[1] != -1)):
    #if delYaw , delPitch greater than angle threshold.
    for i in range(numpts):
      trajList.append([0, i*delPitch/(numpts-1), i*delYaw/(numpts-1)])

  # if no obj detected.
  else:
    for i in range(numpts):
      trajList.append([0, 0, 0])


  return trajList



def madFilter(dataArr, threshold =3):
  """
  (list),(float) -> (float)
  Description: Calculate of the last point is an outlier depending on the threshold among the given set of points and returns the value that  should be replaced if it is an outlier. 
  >>> sampleVal = madFilter([5,4,4,4,4,5,3,3,1,1,2,2,5])
  >>> sampleVal
  5
  """
  assert (type(dataArr) == list),'Please input a list of nos'
  bArr = []
  medianVal = statistics.median(dataArr)
  for element in dataArr:
    bArr.append(abs(medianVal - element))
  madValue =  statistics.median(bArr)
  if(bArr[-1] > threshold*madValue):
    return medianVal
  else :
    return dataArr[-1]

  

def spline6pt(y):
  """
  (np.array[] (size = 6) ) -> (list[4])
  Description: Generates peicewise spline curves for the 6 y pts, with x pts equally spaced as x[0:5].
  Outputs the coeffs last piecewise curves ie coeffnew. ie ( coeffx = ax, bx, cx, dx)

  regenrate the splines example ( for ref of abcd ignore rest) 
  y = a2 + b2*(x-2) + c2*(x-2)**2 + d2*(x-2)**3
  
  Similarly for coeff 3 for x betn 3,4 as 
  y = a3 + b3*(x-3) + c3*(x-3)**2 + d3*(x-3)**3
  >>>
  """
  # if a valid entry 
  if( y.size == 6):
    #logging.info("reached spline 6pt")
    x = np.array([0, 1, 2, 3, 4, 5])
    cs = CubicSpline(x,y,bc_type='natural')

    # Polynomial coefficients for 4 < x <= 5 ie the last curve among 6 pts.
    a4 = cs.c.item(3,4)
    b4 = cs.c.item(2,4)
    c4 = cs.c.item(1,4)
    d4 = cs.c.item(0,4)

    coeff4 = [a4, b4 , c4, d4 ]
    #logging.info(str(coeff4))
    return coeff4


def cam_grabber_thread(event, source = VID_SRC, imgQ = imageQ):
    """
    (int, queue) -> NoneType
    Description : Grabs the image and puts it into the imageQ buffer.
    """
    cap = cv2.VideoCapture(source)
    time.sleep(3.0)
    grabberLock = threading.Lock()
    imgQ_size = imgQ.qsize()
    frame_counter = 1
    
    while not event.is_set():
        
        start_time = time.time() # start time of the loop
        
        imgQ_size = imgQ.qsize()
        #logging.info(" no of frames"  + str(imgQ_size))
        
        grabbed, frame = cap.read()
        
        # sending every nth frame to process.
        if(frame_counter == PROC_FRAME_FREQ):
        # to make sure the buffer does not lag as real time as possible.
          if(imgQ_size < MAX_NO_FRAMES):
            with grabberLock:
              pass
              imgQ.put(frame)
          frame_counter = 1
          #logging.info("FPS frame grab: " + str(1.0 / (time.time() - start_time))) # FPS = 1 / time to process loop
          
        else: 
          frame_counter = frame_counter + 1
        #logging.info("FPS frame grab: " + str(1.0 / (time.time() - start_time))) # FPS = 1 / time to process loop
        
    cap.stop()
    cap.release()


def video_grabber_thread(event, source = VID_SRC, imgQ = imageQ):
    
  cap = cv2.VideoCapture(VIDEO_SOURCE)
  time.sleep(3.0)
  grabberLock = threading.Lock()
  imgQ_size = imgQ.qsize()
  frame_counter = 1
  while(cap.isOpened() and (not event.is_set())):
    start_time = time.time() # start time of the loop

    imgQ_size = imgQ.qsize()
    #logging.info(" no of frames"  + str(imgQ_size))
    ret, frame = cap.read()
    if(frame_counter == PROC_FRAME_FREQ):
    # to make sure the buffer does not lag as real time as possible.
      if(imgQ_size < MAX_NO_FRAMES):
        with grabberLock:
          pass
          imgQ.put(frame)
      frame_counter = 1
      logging.info("FPS video grab: " + str(1.0 / (time.time() - start_time))) # FPS = 1 / time to process loop
        
    else: 
      frame_counter = frame_counter + 1
    time.sleep(0.01)  # to avoid this thread taking all control of CPU

    #logging.info("FPS frame grab: " + str(1.0 / (time.time() - start_time))) # FPS = 1 / time to process loop
    
  cap.stop()
  cap.release()
  cv2.destroyAllWindows()


#def show_frame(frame, event):
#  while not event.is_set():

def sendParams(objArea, objCX, objCY):
  """
  (double, int, int) ->NoneType
  @brief : Sends area , obj cx , and obj cy to stm32 MCU.
  >>> sendParams(100, 123, 441)
  """ 
  params = ("<"+str(objArea)+', '+str(objCX)+', '+str(objCY)+">")
  stcom.sendToArduino(params.encode('utf-8'))
  

def sendCoeffs(coeffx, coeffy):
  """
  (list[], list[], list[], list[], list[], list[] size = 4each) -> NoneType
  description : Sends spline coeffcients to the MCU 
  """
  
  """
  Coeffs = ("<"\
  +cx2[1]+','+cx2[2]+','+cx2[3]+','+cx2[4]+','\
  +cx3[1]+','+cx3[2]+','+cx3[3]+','+cx3[4]+','\
  +cx4[1]+','+cx4[2]+','+cx4[3]+','+cx4[4]+','\

  +cy2[1]+','+cy2[2]+','+cy2[3]+','+cy2[4]+','\
  +cy3[1]+','+cy3[2]+','+cy3[3]+','+cy3[4]+','\
  +cy4[1]+','+cy4[2]+','+cy4[3]+','+cy4[4]+','\
  +">")
  #"""
  Coeffs = str('<'\
  +str(coeffx[0])+','+str(coeffx[1])+','+str(coeffx[2])+','+str(coeffx[3])+','\
  +str(coeffy[0])+','+str(coeffy[1])+','+str(coeffy[2])+','+str(coeffy[3])+','\
  +'>')
  #logging.info('<'+str(coeffx[1])+','+str(coeffx[2])+','+str(coeffx[3])+',')
  #logging.info("<"+str(coeffx[1])+',')
  
  #Coeffs = str('<'+str(coeffx[1])+','+str(coeffx[2])+','+str(coeffx[3])+','+str(coeffx[4]) )
  stcom.sendToArduino(Coeffs.encode('utf-8'))


def process_thread(event, source = VID_SRC, trajQ = commQ, imgQ = imageQ):
  """
  @brief : pops imgQ process img and calc gimb trajectory and sets the event.
  """
  objA = 0
  objCX = 0
  objCY = 0
  old_objA = 0
  old_objCX = 0
  old_objCY = 0
  frame_cx_buffer = np.array([0,0,0,0,0,0])
  frame_cy_buffer = np.array([0,0,0,0,0,0])
  coeffx_new = [0,0,0,0]
  coeffy_new = [0,0,0,0]
  logFile = open("logAngles.txt", "w")
  counter_comms_update = 1
  processLock = threading.Lock()
  trajList = []
  FILTERBUFFERSIZE = 15
  filterdataBufferYaw = [0]*FILTERBUFFERSIZE
  filterdataBufferPitch = [0]*FILTERBUFFERSIZE
  filterdataBufferRoll = [0]*FILTERBUFFERSIZE # not useful as of now
  FILTEREDYAW = 0
  FILTEREDPITCH = 0
  while(1):
    if not imgQ.empty():
      start_time_proc = time.time()
      frame = imgQ.get()
      logging.info(" no of process frames "  + str(imgQ.qsize()))
      
      ## May edit to zero if default cam is set to 0
      if CAMERA_AVAIL == True:
        if (source != -1):
          frame =  cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)

      objA, objCX, objCY = GBT.trackGreenBall(frame)

      # Shifting and Updating 1 element at a time. values according to gimbal <S. 
      frame_cx_buffer[0:5] = frame_cx_buffer[1:6]
      frame_cy_buffer[0:5] = frame_cy_buffer[1:6]

      if(objCX != -1):
        frame_cx_buffer[5] = (FRAME_CX - objCX)/(PIX_PER_DEG+PIX_PER_DEG_VAR)
      else:
        frame_cx_buffer[5] = 0

      if(objCY != -1 ):
        frame_cy_buffer[5] = (FRAME_CY - objCY )/(PIX_PER_DEG+PIX_PER_DEG_VAR)
      else:
        frame_cy_buffer[5] = 0

      #logging.info(str(objA) + " " +str(objCX) + " " +str(objCY) + " " +str(frame_cx_buffer[5]) + " " +str(frame_cy_buffer[5]) )
      
      # Filtering the data MAD filter
      
      filterdataBufferYaw[0:(FILTERBUFFERSIZE-1)] = filterdataBufferYaw[1:FILTERBUFFERSIZE]
      filterdataBufferYaw[(FILTERBUFFERSIZE-1)] = frame_cx_buffer[5]
      print(type(filterdataBufferYaw))
      print(len(filterdataBufferYaw))
      #newVal = madFilter(filterdataBufferYaw) BUG here
      #print("newVal is " + str(newVal))
      #frame_cx_buffer[5] = madFilter(filterdataBufferYaw)
      '''
      FILTEREDYAW = frame_cx_buffer[5]

      filterdataBufferPitch[0:(FILTERBUFFERSIZE-1)] = filterdataBufferPitch[1:FILTERBUFFERSIZE]
      filterdataBufferPitch[(FILTERBUFFERSIZE-1)] = frame_cx_buffer[5]
      frame_cy_buffer[5] = madFilter(filterdataBufferPitch)
      FILTEREDPITCH = frame_cy_buffer[5]
      '''
      coeffx_new = spline6pt(frame_cx_buffer) # 4 coeffs for piecewise curve using six pts as a support.
      coeffy_new = spline6pt(frame_cy_buffer) # 4 coeffs for piecewise curve using six pts as a support.
          
      #  #logging.info("newYaw v alue " + str(new_yawValue))
      new_yawValue = coeffx_new[0] + coeffx_new[1]*1 + coeffx_new[2]*1**2 + coeffx_new[3]*1**3
      new_pitchValue = coeffy_new[0] + coeffy_new[1]*1 + coeffy_new[2]*1**2 + coeffy_new[3]*1**3
      
      if(LOG_FILES == True):
        nowTime = time.strftime('%d-%m-%Y %H:%M:%S')
        logInfoStr = '{0}, {1}, {2}, {3}, {4}, {5}, {6} \n'.format(nowTime,frame_cx_buffer[5],FILTEREDYAW,new_yawValue,frame_cy_buffer[5],FILTEREDPITCH,new_pitchValue )
        logFile.write(str(logInfoStr))
        logging.info(logInfoStr)
        #logFile.write(str(nowTime) +", " +  str(new_yawValue) + ", " + str(new_pitchValue)+'\n')
      #print(str(new_yawValue))
      
      with processLock:
        if INCLUDE_STM == True:
          sendCoeffs(coeffx_new,coeffy_new)
          counter_comms_update = 1
      #logging.info("size of " + str(trajQ.qsize()))

      #logging.info("size of commsQ" + str(trajQ.qsize()))
      cv2.imshow("Process Frame", frame)
      if cv2.waitKey(1) == ord("q"):
        event.set()
        cv2.destroyAllWindows()
        if(LOG_FILES == True):
          logFile.close()
        break
      #logging.info("runtime process : " + str( (time.time() - start_time_proc))) # FPS = 1 / time to process loop
      #logging.info("FPS process : " + str(1.0 / (time.time() - start_time_proc))) # FPS = 1 / time to process loop

    #cv2.destroyAllWindows()
    #"""




""" START YOUR CODE HERE """

if __name__ == '__main__':
  pass
  
  print
  print
  event = threading.Event()
    
  format = "%(asctime)s: %(message)s"
  logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")
  if INCLUDE_STM == True:
    logging.info("Waiting for arduino.")
    stcom.waitForArduino()
    logging.info("Arduino ready.")
  #grab_th = threading.Thread(target = grabber_thread())
  #proc_th = threading.Thread(target = process_thread())
  #proc_th.start()
  #grab_th.start()

  # Takes care of joining, threads, ie main wont after this until all threads are finished.
  if CAMERA_AVAIL == True:
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
      executor.submit(process_thread, event)
      executor.submit(cam_grabber_thread, event)

  if CAMERA_AVAIL == False:
    print("please press q before video ends or quit from task manager")
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
      executor.submit(process_thread, event)
      executor.submit(video_grabber_thread, event)

  # useless cause of threadpoolExec  
  time.sleep(7)
  event.set()
  #  executor.submit(f2)
  
  #time.sleep(5.0)
  #event.set()
  # waits until I receive a message Arduino ready from arduino setup part.
  # Obcomp should be ready first follwed by the duino.
  #print("waiting for arduino response.")
  #ComArduino2.waitForArduino()
  #print("stm read successfully. LED should be blinking.")
  
  # creating an empty buffer list.
  #gimbal_coords_buffer = []


  #gimbal_coords_buffer.append("<100,200,0.2>")
  #gimbal_coords_buffer.append("<101,200,0.2>")
  #gimbal_coords_buffer.append("<102,200,0.2>")
  #gimbal_coords_buffer.append("<103,200,0.2>")
  #gimbal_coords_buffer.append("<104,200,0.2>")


  #ComArduino2.runTest(gimbal_coords_buffer)
  

  #while (1):
  #  if cv2.waitKey(1) == ord("q"):
  #    event.set()
  #    cv2.destroyAllWindows()
  #      ball_tracking.live_tracking()
        #key = cv2.waitKey(1) & 0xFF
        #if key == ord("q"):
        #      break
        #ball_tracking.vs.stop()
        #cv2.destroyAllWindows()
  #import doctest
  #doctest.testmod()
  
  
  
  
""" END OF FILE """

