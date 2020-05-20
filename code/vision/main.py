"""
 Author: Param Deshpande
 Date created:  Mon 27 Apr 18:11:03 IST 2020
 Description: 
 Main jetson/pc python file for controlling gimbal via the tracked object.
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
 
if __name__ == '__main__':
  import concurrent.futures
  import logging
  import queue
  import random
  import threading
  import serial
  import time
  #import ball_tracking
  import cv2
  import ComArduino2 as stcom
  import greenBallTracker as GBT 
  #import 



""" WRITE YOUR VARIABLES HERE """

NO_OF_PTS = 3

CHANGE_YAW_THOLD = 2
CHANGE_PITCH_THOLD = 2
THRES_PERCENT_CHANGE =0.10
VID_SRC = 2

FRAME_CX = 460/2
FRAME_CY = 639/2

PIX_PER_DEG = 18.0
PIX_PER_DEG_VAR = 1.3

MAX_NO_FRAMES = 10

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
  Description:generates trajectory for delta gimbal <s, 
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
  
  if((newXY[0] is not -1) and (newXY[1] is not -1)):
    #if delYaw , delPitch greater than angle threshold.
    for i in range(numpts):
      trajList.append([0, i*delPitch/(numpts-1), i*delYaw/(numpts-1)])

  # if no obj detected.
  else:
    for i in range(numpts):
      trajList.append([0, 0, 0])


  return trajList

  

#def ...:
#  """
#  () -> ()
#  Description: 
#  >>>
#  
#  """

def grabber_thread(event, source = VID_SRC, imgQ = imageQ):
    """
    (int, queue) -> NoneType
    Description : Grabs the image and puts it into the imageQ buffer.
    """
    cap = cv2.VideoCapture(source)
    time.sleep(3.0)
    grabberLock = threading.Lock()
    imgQ_size = imgQ.qsize()
    while not event.is_set():
        
        start_time = time.time() # start time of the loop
        
        imgQ_size = imgQ.qsize()
        logging.info(" no of frames"  + str(imgQ_size))
        
        grabbed, frame = cap.read()
        
        # to make sure the buffer does not lag as real time as possible.
        if(imgQ_size < MAX_NO_FRAMES):
          with grabberLock:
            pass
            imgQ.put(frame)
        
        #logging.info("frame grab runtime" + str(time.time() - start_time))
        logging.info("FPS frame grab: " + str(1.0 / (time.time() - start_time))) # FPS = 1 / time to process loop
        

    cap.stop()
    cap.release()


#def show_frame(frame, event):
#  while not event.is_set():


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
  processLock = threading.Lock()
  trajList = []
  while(1):
    if not imgQ.empty():
      start_time_proc = time.time()
      frame = imgQ.get()
      #logging.info(" no of process frames"  + str(imgQ.qsize()))
      
      if (source is not 0):
        frame =  cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
      
      old_objA, old_objCX, old_objCY = objA, objCX, objCY
      objA, objCX, objCY = GBT.trackGreenBall(frame)
      logging.info(str(objA) + " " +str(objCX) + " " +str(objCY))

      with processLock:
        pass
        trajList = trajectoryGen((FRAME_CX, FRAME_CY), (objCX, objCY))
        trajQ.put(trajList)

      #logging.info("size of commsQ" + str(trajQ.qsize()))
      cv2.imshow("Process Frame", frame)
      if cv2.waitKey(1) == ord("q"):
        event.set()
        cv2.destroyAllWindows()
        break
      #logging.info("runtime process : " + str( (time.time() - start_time_proc))) # FPS = 1 / time to process loop
      logging.info("FPS process : " + str(1.0 / (time.time() - start_time_proc))) # FPS = 1 / time to process loop
    
    #cv2.destroyAllWindows()
    #"""


# We are sending roll. pitch, yaw to the MCU.
def comms_thread(event,trajQ = commQ):
  """
  (list) -> (NoneType)
  Description: Sends gimbal traj to mcu and waits for ack.
  >>>
  
  """
  ptTrajList = []
  dataRecvd = ''
  while not event.is_set() :

    # if there is a new list of trajectory in the Queue. 
    if trajQ.qsize() > 0.0:
      start_time_comms = time.time()
      ptTrajList = trajQ.get()
      logging.info("trajQ size after "+str(trajQ.qsize()))
      
      ## start sending vals one by one and wait for ack by mcu.
      for i in range(len(ptTrajList)):
        gimbal_coords_buffer = []
        gimbal_coords_buffer.append("<"+str(ptTrajList[i][0])+', '+str(ptTrajList[i][1])+', '+str(ptTrajList[i][2])+">")
        teststr = gimbal_coords_buffer[0]
        logging.info(teststr)
        stcom.sendToArduino(teststr.encode('utf-8'))
        while(dataRecvd != ACK_MCU_MSG):
          dataRecvd = stcom.recvFromArduino()
        #stcom.runTest(gimbal_coords_buffer)
      
      time.sleep(0.02) #10ms for receive from stm.
      #time.sleep(0.05) #5ms for receive from stm.
       
      #logging.info("comms runtime " + str(time.time() - start_time_comms) )
      logging.info("FPS comms : " + str(1.0 / (time.time() - start_time_comms))) # FPS = 1 / time to process loop


""" START YOUR CODE HERE """

if __name__ == '__main__':
  pass

  print
  print
  event = threading.Event()
    
  format = "%(asctime)s: %(message)s"
  logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")

  logging.info("Waiting for arduino.")
  stcom.waitForArduino()
  logging.info("Arduino ready.")
  #grab_th = threading.Thread(target = grabber_thread())
  #proc_th = threading.Thread(target = process_thread())
  #proc_th.start()
  #grab_th.start()

  # Takes care of joining, threads, ie main wont after this until all threads are finished.
  with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
    executor.submit(process_thread, event)
    executor.submit(grabber_thread, event)
    executor.submit(comms_thread, event)
  
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

