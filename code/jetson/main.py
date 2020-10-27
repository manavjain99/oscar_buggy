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

INCLUDE_STM = True
LOG_FILES = True

if __name__ == '__main__':
  import numpy as np
  import concurrent.futures
  import logging
  import queue
  import random
  import threading
  import serial
  import time
  import cv2
  import statistics 
  import signal
  import socket
  from scipy.interpolate import CubicSpline
  from enum import Enum 
  
  import greenBallTracker as GBT 
  import aruco_tracking as ART
  import curveplanner as CPLN
  import goproAlive

  if INCLUDE_STM == True:
    import ComArduino2 as stcom
  
""" WRITE YOUR VARIABLES HERE """

class INPUT_FEED(Enum):
  VIDEO_FILE, GOPRO_STREAM, WEBCAM = range(3)

# Choose among the Three VIDEO_FILE, GOPRO_STREAM, WEBCAM 
IP_FEED = INPUT_FEED.GOPRO_STREAM


####### EXTERNAL FILES ##########
#VIDEO_SOURCE = "ball_tracking_example.mp4"
VIDEO_SOURCE = "../tests/aruco.mp4"
SPLINE_COEFFS_LOG = "../pilotdash/splineCoeffs.txt"
GIMBAL_ANGLES_LOG = "../pilotdash/logAngles.txt"
LOCALHOST_STREAM_URI = "udp://127.0.0.1:10000"

####### CAMERA AND FRAMES PARAMS #########
# 3, 2, 1 for ext webcam 0 for webcam use camtesting.py in tests directly 
WEBCAM_INDEX = 2
#Laptop Webcam 
#FRAME_CX = 480.0/2.0
#FRAME_CY = 640.0/2.0

# external Webcam 
FRAME_CX = 480.0/2.0
FRAME_CY = 640.0/2.0

# Pixels to Degree conversion . 
MULTIPLICATION_FACTOR = 1.5
PIX_PER_DEG = 18.0
PIX_PER_DEG_VAR = 1.3

# Max queue size 
MAX_NO_FRAMES = 10000

# ie processing every nth frame, depending on the Input FPS you may want to tweak this settings. 
PROC_FRAME_FREQ = 3

# need not change these vars.
MAX_DEL_YAW =   MULTIPLICATION_FACTOR*FRAME_CX/(PIX_PER_DEG+PIX_PER_DEG_VAR)
MAX_DEL_PITCH = MULTIPLICATION_FACTOR*FRAME_CY/(PIX_PER_DEG+PIX_PER_DEG_VAR)

########## PROCESS PARAMS #############
# Avoid changing this change the number of process frames frequency instead.  
SPLINE_FRAME_SIZE = 6 

# mad Filter rejects outliers, may need tuning from feed to feed. 
FILTER_ANGLES = False

######## THREADS AND OTHER VALUES ########
imageQ = queue.Queue(maxsize=10000)
commQ = queue.Queue(maxsize=30000)
GlobalEvent = threading.Event()

""" WRITE YOUR FUNCTIONS HERE """

current_milli_time = lambda: int(round(time.time() * 1000))
epochTimeMillis = current_milli_time()


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

def frame_grabber_thread(event, imgQ = imageQ):
  """
  (event, queue) -> NoneType
  Description : Grabs the image from respective sources and puts it into the imageQ buffer.
  """
  if IP_FEED == INPUT_FEED.VIDEO_FILE :
    cap = cv2.VideoCapture(VIDEO_SOURCE)
  elif IP_FEED == INPUT_FEED.WEBCAM :
    cap = cv2.VideoCapture(WEBCAM_INDEX)
  elif IP_FEED == INPUT_FEED.GOPRO_STREAM :
    cap = cv2.VideoCapture(LOCALHOST_STREAM_URI)

  time.sleep(1.0)
  grabberLock = threading.Lock()
  imgQ_size = imgQ.qsize()
  frame_counter = 1
  
  while(cap.isOpened() and (not event.is_set())):
    start_time = time.time() # start time of the loop
    imgQ_size = imgQ.qsize()
    #logging.info(" no of frames"  + str(imgQ_size))
    ret, frame = cap.read()
  
    if(frame_counter == PROC_FRAME_FREQ):
    # to make sure the buffer does not lag, as real time as possible.
      if(imgQ_size < MAX_NO_FRAMES):
        with grabberLock:
          pass
          imgQ.put(frame)
      frame_counter = 1
      logging.info("inst FPS frame grab: " + str(1.0 / (time.time() - start_time))) # FPS = 1 / time to process loop
    else: 
      frame_counter += 1
    if IP_FEED == INPUT_FEED.VIDEO_FILE:
      time.sleep(0.01)  # to avoid this thread taking all control of CPU


def sendParams(objArea, objCX, objCY):
  """
  (double, int, int) ->NoneType
  @brief : Sends area , obj cx , and obj cy to stm32 MCU.
  >>> sendParams(100, 123, 441)
  """ 
  params = ("<"+str(objArea)+', '+str(objCX)+', '+str(objCY)+">")
  stcom.sendToArduino(params.encode('utf-8'))

def appendCoeffs(Coeffs, coeffv, coeffw, coeffx, coeffy):
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
  limF = lambda a: (float("{:7.3f}".format(a)))
  # ie the floats are $$$$.$$$ format.
  # Yes the space helpsme parse it / dont remove. 
  Coeffs += str(" "\

  +str(limF(coeffv[0]))+','\
  +str(limF(coeffv[1]))+','\
  +str(limF(coeffv[2]))+','\
  +str(limF(coeffv[3]))+','\

  +str(limF(coeffw[0]))+','\
  +str(limF(coeffw[1]))+','\
  +str(limF(coeffw[2]))+','\
  +str(limF(coeffw[3]))+','\

  +str(limF(coeffx[0]))+','\
  +str(limF(coeffx[1]))+','\
  +str(limF(coeffx[2]))+','\
  +str(limF(coeffx[3]))+','\

  +str(limF(coeffy[0]))+','\
  +str(limF(coeffy[1]))+','\
  +str(limF(coeffy[2]))+','\
  +str(limF(coeffy[3]))\

  +" ; ")
  return Coeffs
  # Yes the space helpsme parse it / dont remove. 
  #logging.info('<'+str(coeffx[1])+','+str(coeffx[2])+','+str(coeffx[3])+',')
  #logging.info("<"+str(coeffx[1])+',')
  
  #Coeffs = str('<'+str(coeffx[1])+','+str(coeffx[2])+','+str(coeffx[3])+','+str(coeffx[4]) )
  #stcom.sendToArduino(Coeffs.encode('utf-8'))
  #lo.......................................................................................................................................gging.info((Coeffs))

def sendMsg(myMsg):
  """
  Sends EOL & the entire Msg ie 'q' character to the Arduino board. 
  """
  myMsg += str('q')
  logging.info((myMsg))
  stcom.sendToArduino(myMsg.encode('utf-8'))

def appendSPACE(initMsg):
  """
  Appends SPACE ie ' ' character to the Arduino board. easier for parsing.  
  """
  initMsg += str(' ')
  return initMsg
  #stcom.sendToArduino(mySPACE.encode('utf-8'))

def process_thread(event, source = WEBCAM_INDEX, trajQ = commQ, imgQ = imageQ):
  """
  @brief : pops imgQ process img and calc gimb trajectory and sets the event.
  """
  ########THREAD SPECIFIC PARAMS ################
  processLock = threading.Lock()
  logFile = open(str(GIMBAL_ANGLES_LOG), "w")
  logFileCoeffs = open(SPLINE_COEFFS_LOG, "w")
  counter_comms_update = 1
  # Counts how many times has the frame/while loop run RESETS ONCE IT HITS SPLINE_FRAME_SIZE
  curveplanner_iterator_ = 0 
  ##############################################

  ###### OBJECT STORING PARAMS INIT ############
  objA = 0  #area
  objR = 0  # rotation 
  objCX = 0 # center x
  objCY = 0 # center y
  # oframe stands for object frame ie a frame with object present in it.
  oframe_ca_buffer = np.zeros(SPLINE_FRAME_SIZE) # area 
  oframe_cr_buffer = np.zeros(SPLINE_FRAME_SIZE) # roll
  oframe_cp_buffer = np.zeros(SPLINE_FRAME_SIZE) # pitch
  oframe_cy_buffer = np.zeros(SPLINE_FRAME_SIZE) # yaw  
  coeff_area = []  # unused kept as a buffer for future development 
  coeff_roll = []  # Set of piecewise coeffs returned of len (SPLINE_FRAME_SIZE)
  coeff_pitch = [] # Set of piecewise coeffs returned of len (SPLINE_FRAME_SIZE)
  coeff_yaw = []   # Set of piecewise coeffs returned of len (SPLINE_FRAME_SIZE)
  #############################################
  ########## MAD FILTER VARS INIT ###########
  FILTERBUFFERSIZE = 15 # How many values to filter from ie MAD of how many vals 
  filterdataBufferYaw = [0]*FILTERBUFFERSIZE
  filterdataBufferPitch = [0]*FILTERBUFFERSIZE
  filterdataBufferRoll = [0]*FILTERBUFFERSIZE # not useful as of now
  FILTEREDYAW = 0
  FILTEREDPITCH = 0
  ###########################################
  logging.info("Process thread init success")

  while(1):
    if not imgQ.empty():
      start_time_proc = time.time()
      frame = imgQ.get()
      #logging.info(" no of process frames "  + str(imgQ.qsize()))
      
      ## May edit to source != zero if default cam is set to 0
      if IP_FEED == INPUT_FEED.WEBCAM:
        if (source != -1):
          frame =  cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)

      if IP_FEED == INPUT_FEED.GOPRO_STREAM:
        frame =  cv2.rotate(frame, cv2.ROTATE_180)


      #####  choose your tracking algo  here ##############
      
      objA, objR, objCX, objCY = ART.trackArucoMarker(frame)
      #logging.info(" got params as " + str(objA) + " " + str(objR) +" " + str(objCX) + " " + str(objCY))
      ############## LOADING ....*VALID* PARAMS INTO BUFFER ##########
      if( objA != -1):
        curveplanner_iterator_ += 1
        ocyclic_index = curveplanner_iterator_ - 1
        #logging.info("curve planner iterator is " + str(curveplanner_iterator_))
        if(curveplanner_iterator_ == 1):
          # Making first and last elem same to avoid discontinuities in every hyperframe's output
          oframe_cr_buffer[0] = oframe_cr_buffer[-1]   
          oframe_cp_buffer[0] = oframe_cp_buffer[-1]   
          oframe_cy_buffer[0] = oframe_cy_buffer[-1]   

        else:
        # Zero o/p if obj not detected converting from pixels to angs 
          oframe_cr_buffer[ocyclic_index] = 0 #for future planning ...
          oframe_cy_buffer[ocyclic_index] = (FRAME_CX - objCX)/(PIX_PER_DEG+PIX_PER_DEG_VAR) if(objCX != -1) else 0.0
          oframe_cp_buffer[ocyclic_index] = (FRAME_CY - objCY)/(PIX_PER_DEG+PIX_PER_DEG_VAR) if(objCY != -1) else 0.0

        #logging.info(" got frame x buffer as  " + str(oframe_cy_buffer) + " got frame y buffer as  " + str(oframe_cp_buffer) )
        #logging.info(str(objA) + " " +str(objCX) + " " +str(objCY) + " " +str(oframe_cy_buffer[5]) + " " +str(oframe_cp_buffer[5]) )
        
        ######## Filtering the data MAD filter ################
        # DONT COMMENT OUT STUFF YOU DONT KNOW # 
        if FILTER_ANGLES == True:
          filterdataBufferPitch[0:(FILTERBUFFERSIZE-1)] = filterdataBufferPitch[1:FILTERBUFFERSIZE]
          filterdataBufferPitch[(FILTERBUFFERSIZE-1)] = oframe_cy_buffer[ocyclic_index]
  
          filterdataBufferYaw[0:(FILTERBUFFERSIZE-1)] = filterdataBufferYaw[1:FILTERBUFFERSIZE]
          filterdataBufferYaw[(FILTERBUFFERSIZE-1)] = oframe_cy_buffer[ocyclic_index]
          #print(type(filterdataBufferYaw))
          #print(len(filterdataBufferYaw))
          #newVal = madFilter(filterdataBufferYaw)
          #print("newVal is " + str(newVal))

          ###### THIS PART IS WHERE FILTERING HAPPENS ############## 
          UNFILTEREDYAW = oframe_cy_buffer[ocyclic_index]
          UNFILTEREDPITCH = oframe_cp_buffer[ocyclic_index]
          oframe_cy_buffer[ocyclic_index] = madFilter(filterdataBufferYaw)
          oframe_cp_buffer[ocyclic_index] = madFilter(filterdataBufferPitch)
        
        ############# GET THE CURVES HERE #################
        if (curveplanner_iterator_ == SPLINE_FRAME_SIZE):
          curveplanner_iterator_ = 0
          coeff_area = CPLN.getBsplineCoeffs(oframe_cr_buffer) # 0s for now. do whatever you want to do, using 4 values per piecewise spline
          coeff_roll = CPLN.getBsplineCoeffs(oframe_cr_buffer)  # its just zeros ... for now 
          coeff_pitch = CPLN.getBsplineCoeffs(oframe_cp_buffer) # set of piecewise coeffs [[dcba0],[dcba1], ..]
          coeff_yaw = CPLN.getBsplineCoeffs(oframe_cy_buffer) # set of piecewise coeffs [[dcba0],[dcba1], ..]
          #coeff_yaw = spline6pt(oframe_cy_buffer) # 4 coeffs for piecewise curve using six pts as a support.
          #coeff_pitch = spline6pt(oframe_cp_buffer) # 4 coeffs for piecewise curve using six pts as a support.
        
          if(LOG_FILES == True):
            # Justifies the op to $$$$.$$$ nos where $ may be space or number.
            limF = lambda a: (float("{:7.3f}".format(a)))

            for coeffs_a,coeffs_r,coeffs_p,coeffs_y in zip(coeff_area, coeff_roll, coeff_pitch, coeff_yaw):  
              nowTimeMillis = current_milli_time() - epochTimeMillis
              # time , raw algo pitch, filtered pitch, raw algo yaw, filtered yaw,
              if FILTER_ANGLES == True:
                logInfoStr = '{0},\t {1},\t {2},\t {3},\t {4},\t \n'.format(\
                nowTimeMillis,\
                UNFILTEREDPITCH,oframe_cp_buffer[ocyclic_index],\
                UNFILTEREDYAW  ,oframe_cy_buffer[ocyclic_index] )
                logFile.write(str(logInfoStr))

              # time , d ,c , b, a for (x)
              logCoeffStr = '{0},\t {1},\t {2},\t {3},\t {4},\t {5},\t {6},\t {7},\t {8},\t {9},\t {10},\t {11},\t {12},\t {13},\t {14},\t {15},\t {16}\t \n'.format(\
              nowTimeMillis,\
              limF(coeffs_a[0]),limF(coeffs_a[1]),limF(coeffs_a[2]),limF(coeffs_a[3]),\
              limF(coeffs_r[0]),limF(coeffs_r[1]),limF(coeffs_r[2]),limF(coeffs_r[3]),\
              limF(coeffs_p[0]),limF(coeffs_p[1]),limF(coeffs_p[2]),limF(coeffs_p[3]),\
              limF(coeffs_y[0]),limF(coeffs_y[1]),limF(coeffs_y[2]),limF(coeffs_y[3])\
              )

              logFileCoeffs.write(str(logCoeffStr))
              
              #logging.info(logInfoStr)
              #logFile.write(str(nowTime) +", " +  str(new_yawValue) + ", " + str(new_pitchValue)+'\n')
              #print(str(new_yawValue))
          
          ########### CRITICAL SECTION SENDING VALS UART AND QUEUES #########
          with processLock:
            if INCLUDE_STM == True:
              paramsMsg = str(" ")
              paramsMsg = appendSPACE(paramsMsg)
              for coeffs_a,coeffs_r,coeffs_p,coeffs_y in zip(coeff_area, coeff_roll, coeff_pitch, coeff_yaw):  
                paramsMsg = appendCoeffs(paramsMsg,coeffs_a,coeffs_r,coeffs_p,coeffs_y)
                counter_comms_update = 1
              sendMsg(paramsMsg) 
          #logging.info("size of " + str(trajQ.qsize()))
          #################################################################

        #logging.info("size of commsQ" + str(trajQ.qsize()))
        #logging.info("runtime process : " + str( (time.time() - start_time_proc))) # FPS = 1 / time to process loop
        logging.info("FPS process : " + str(1.0 / (time.time() - start_time_proc))) # FPS = 1 / time to process loop

def keyboardInterruptHandler(signal, frame):
  GlobalEvent.set()
  print("KeyboardInterrupt (ID: {}) has been caught. Cleaning up...".format(signal))
  exit(0)

def main():
  print
  print
  signal.signal(signal.SIGINT, keyboardInterruptHandler)
  
  format = "%(asctime)s: %(message)s"
  logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")
  print("press ctrl+c twice to exit. ")
  if INCLUDE_STM == True:
    logging.info("Waiting for arduino.")
    stcom.waitForArduino()
    logging.info("Arduino ready.")
  # Takes care of joining, threads, ie main wont after this until all threads are finished.
  with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
    executor.submit(process_thread, GlobalEvent)
    executor.submit(frame_grabber_thread, GlobalEvent)   
    if IP_FEED == INPUT_FEED.GOPRO_STREAM:
      



""" START YOUR CODE HERE """

if __name__ == '__main__':
  pass
  main()  
    
""" END OF FILE """